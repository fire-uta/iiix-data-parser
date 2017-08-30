from functools import reduce


from numpy import uint16
from numpy import bool_


from query_result_list import QueryResultList
from data_record import DataRecord
from has_actions import HasActions
from session import Session
from filterable import Filterable
from has_documents import HasDocuments


from attr_utils import _memoize_attr


class Query(DataRecord, HasActions, Filterable, HasDocuments):
  def __init__(self, query_id, topic = None, user = None, condition = None, autocomplete = None, query_text = None, session = None, precision = None):
    DataRecord.__init__( self, str(query_id) )
    HasDocuments.__init__( self )
    self.topic = topic
    self.user = user
    self.condition = condition
    self.autocomplete = bool_(autocomplete)
    self.query_text = query_text
    self.session = session
    self.precision = precision
    self.result_list = QueryResultList(self)

  def _rank_sanity_check(self, rank):
    if int(rank) < 1 or int(rank) > self.result_list.length():
        raise RuntimeError("Attempted to fetch results up to rank %s for query %s (%s), which is impossible." % (rank, self.record_id, self.query_text))

  def add_to_result_list( self, rank, document ):
    self.result_list.add( rank, document )

  def results_up_to_rank(self, rank, relevance_level=None):
    self._rank_sanity_check(rank)
    return self.result_list.results_up_to_rank(rank, relevance_level=relevance_level)

  def non_relevant_results_up_to_rank(self, rank):
    self._rank_sanity_check(rank)
    return self.result_list.non_relevant_results_up_to_rank(rank)

  def results_of_relevance_level(self, relevance_level):
    return self.results_up_to_rank(self.last_rank_reached(), relevance_level=relevance_level)

  def non_relevant_results(self):
    return self.non_relevant_results_up_to_rank(self.last_rank_reached())

  def moderately_relevant_results_up_to_rank(self, rank):
    self._rank_sanity_check(rank)
    return self.result_list.moderately_relevant_results_up_to_rank(rank)

  def moderately_relevant_results(self):
    return self.moderately_relevant_results_up_to_rank(self.last_rank_reached())

  def highly_relevant_results_up_to_rank(self, rank):
    self._rank_sanity_check(rank)
    return self.result_list.highly_relevant_results_up_to_rank(rank)

  def highly_relevant_results(self):
    return self.highly_relevant_results_up_to_rank(self.last_rank_reached())

  def results_between(self, rank_start, rank_end):
    result_length = self.result_list.length()
    if int(rank_start) < 1 or int(rank_start) > result_length or int(rank_end) < 1 or int(rank_end) > result_length or int(rank_start) > int(rank_end):
        raise RuntimeError("Attempted to fetch results between rank %s and %s for query %s (%s), which is impossible." % (rank_start, rank_end, self.record_id, self.query_text))
    return self.result_list.results_between(rank_start, rank_end)

  def focus_action(self):
    focus_actions = self.actions_by_type('QUERY_FOCUS')
    if len(focus_actions) == 0:
      return (None, None)
    return self.actions_by_type('QUERY_FOCUS')[0]

  def formulation_time_in_seconds(self):
    (idx, query_start_action) = self.focus_action()
    return self.action_duration_in_seconds_for(idx, query_start_action, 'QUERY_ISSUED') if query_start_action is not None else None

  def formulation_event(self):
    (idx, query_start_action) = self.focus_action()
    action_duration = self.action_duration_in_seconds_for(idx, query_start_action, 'QUERY_ISSUED') if query_start_action is not None else None
    return {
        'query_formulation_duration': action_duration,
        'query_formulation_start_at': self.session.seconds_elapsed_at(query_start_action.timestamp) if query_start_action is not None else None,
        'autocomplete': self.autocomplete,
        'query_text': self.query_text,
        'precision': self.precision,
        'average_snippet_scan_duration': self.average_snippet_scanning_time_in_seconds(),
        'query_order_number': self.order_number(),
        'duration_in_seconds': self.duration_in_seconds()
    }

  def last_rank_reached(self):
    return _memoize_attr(
        self,
        '_last_rank_reached',
        lambda: self._calculate_last_rank_reached()
    )

  def _calculate_last_rank_reached(self):
    current_rank_candidate = 1
    for action in reversed(self.actions):
      if hasattr(action, 'rank') and int(action.rank) > current_rank_candidate:
        current_rank_candidate = int(action.rank)
    # Note that this may also return one if there were no actions with a rank.
    # That means the user bailed without doing anything, so it counts as rank 1.
    return current_rank_candidate

  def amount_of_non_relevant_documents_seen_at_last_rank(self):
    return len(self.non_relevant_documents_seen_at_last_rank())

  def non_relevant_documents_seen_at_last_rank(self):
    last_rank = self.last_rank_reached()
    results_seen = self.results_up_to_rank( last_rank )
    return [result.document for result in results_seen if result.is_not_relevant_for_topic( self.topic )]

  def amount_of_contiguous_non_relevant_documents_seen_at_last_rank(self):
    return len(self.last_contiguous_non_relevant_documents_seen())

  def last_contiguous_non_relevant_documents_seen(self):
    last_rank = self.last_rank_reached()
    results_seen = self.results_up_to_rank( last_rank )
    contiguous_non_relevants = []
    for result in reversed(results_seen):
      if result.is_not_relevant_for_topic( self.topic ):
        contiguous_non_relevants.append( result.document )
      else:
        break
    return contiguous_non_relevants

  def total_snippet_scanning_time_in_seconds(self):
    # No actions -> No scanning time.
    if len(self.actions) == 0:
      return None
    formulation_time = self.formulation_time_in_seconds()
    formulation_time = 0 if formulation_time is None else formulation_time  # Act as if formulation was instant
    return self.duration_in_seconds() - formulation_time - sum(self.document_read_times().values())

  def continuous_rank_at(self, rank):
    prior_queries = self.session.queries_prior_to(self)
    prior_last_ranks = [query.last_rank_reached() for query in prior_queries]
    return sum(prior_last_ranks) + rank

  def continuous_rank_at_end(self):
    return self.continuous_rank_at(self.last_rank_reached())

  def order_number(self):
    return self.session.sorted_queries().index(self) + 1

  def rank_of(self, document):
    return self.result_list.rank_of(document)

  @classmethod
  def average_formulation_time_in_seconds(cls, filter_func = lambda query: True):
    queries = list(filter( filter_func, cls.get_store().values() ))
    return reduce( lambda acc, query: acc + query.formulation_time_in_seconds(), queries, 0 ) / len(queries)

  @classmethod
  def average_last_rank_reached(cls, filter_func = lambda query: True):
    queries = list(filter( filter_func, cls.get_store().values() ))
    return reduce( lambda acc, query: acc + float(query.last_rank_reached()), queries, 0.0 ) / float(len(queries))

  @classmethod
  def average_amount_of_non_relevant_documents_seen_at_last_rank(cls, filter_func = lambda query: True):
    queries = list(filter( filter_func, cls.get_store().values() ))
    return reduce( lambda acc, query: acc + float(query.amount_of_non_relevant_documents_seen_at_last_rank()), queries, 0.0 ) / float(len(queries))

  @classmethod
  def average_amount_of_contiguous_non_relevant_documents_seen_at_last_rank(cls, filter_func = lambda query: True):
    queries = list(filter( filter_func, cls.get_store().values() ))
    return reduce( lambda acc, query: acc + float(query.amount_of_contiguous_non_relevant_documents_seen_at_last_rank()), queries, 0.0 ) / float(len(queries))

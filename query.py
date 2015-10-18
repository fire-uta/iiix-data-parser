from numpy import uint16
from numpy import bool_


from query_result_list import QueryResultList
from data_record import DataRecord
from has_actions import HasActions
from session import Session
from filterable import Filterable
from has_documents import HasDocuments


class Query(DataRecord, HasActions, Filterable, HasDocuments):
  def __init__(self, query_id, topic = None, user = None, condition = None, autocomplete = None, query_text = None, session = None, precision = None):
    DataRecord.__init__( self, uint16(query_id) )
    HasDocuments.__init__( self )
    self.topic = topic
    self.user = user
    self.condition = condition
    self.autocomplete = bool_(autocomplete)
    self.query_text = query_text
    self.session = session
    self.precision = precision
    self.result_list = QueryResultList(self)

  def add_to_result_list( self, rank, document ):
    self.result_list.add( rank, document )

  def results_up_to_rank( self, rank ):
    if int(rank) < 1 or int(rank) > self.result_list.length():
        raise RuntimeError("Attempted to fetch results up to rank %s for query %s, which is impossible." % (rank, self.record_id))
    return self.result_list.results_up_to_rank( rank )

  def formulation_time_in_seconds(self):
    (idx, query_start_action) = self.actions_by_type( 'QUERY_FOCUS' )[0]
    return self.action_duration_in_seconds_for( idx, query_start_action, 'QUERY_ISSUED' )

  def last_rank_reached(self):
    current_rank_candidate = 1
    for action in reversed(self.actions):
      if hasattr( action, 'rank' ) and int(action.rank) > current_rank_candidate:
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

  @classmethod
  def average_formulation_time_in_seconds(cls, filter_func = lambda query: True):
    queries = filter( filter_func, cls.get_store().values() )
    return reduce( lambda acc, query: acc + query.formulation_time_in_seconds(), queries, 0 ) / len(queries)

  @classmethod
  def average_last_rank_reached(cls, filter_func = lambda query: True):
    queries = filter( filter_func, cls.get_store().values() )
    return reduce( lambda acc, query: acc + float(query.last_rank_reached()), queries, 0.0 ) / float(len(queries))

  @classmethod
  def average_amount_of_non_relevant_documents_seen_at_last_rank(cls, filter_func = lambda query: True):
    queries = filter( filter_func, cls.get_store().values() )
    return reduce( lambda acc, query: acc + float(query.amount_of_non_relevant_documents_seen_at_last_rank()), queries, 0.0 ) / float(len(queries))

  @classmethod
  def average_amount_of_contiguous_non_relevant_documents_seen_at_last_rank(cls, filter_func = lambda query: True):
    queries = filter( filter_func, cls.get_store().values() )
    return reduce( lambda acc, query: acc + float(query.amount_of_contiguous_non_relevant_documents_seen_at_last_rank()), queries, 0.0 ) / float(len(queries))

import itertools
import numpy


from has_actions import HasActions
from has_queries import HasQueries
from has_documents import HasDocuments


from attr_utils import _memoize_attr


class ActsAsSession(HasActions, HasQueries, HasDocuments):
  def __init__(self, user, topic, condition):
    HasDocuments.__init__(self)
    HasQueries.__init__(self)
    self.user = user
    self.topic = topic
    self.condition = condition

  def average_document_reading_time_in_seconds(self):
    read_times = self.document_read_times()
    return sum(read_times.values()) / len(read_times)

  def average_query_formulation_time_in_seconds(self):
    querying_durations = self.querying_durations()
    return sum(querying_durations) / len(querying_durations)

  def querying_durations(self):
    query_start_actions = self.actions_by_type('QUERY_FOCUS')
    return [self.action_duration_in_seconds_for(idx, action, 'QUERY_ISSUED') for idx, action in query_start_actions]

  def total_query_durations(self):
    return [query.duration_in_seconds() for query in self.queries.values()]

  def last_ranks(self):
    return [query.last_rank_reached() for query in self.queries.values()]

  def amounts_of_non_relevant_docs_seen_at_last_rank(self):
    return [query.amount_of_non_relevant_documents_seen_at_last_rank() for query in self.queries.values()]

  def amounts_of_contiguous_non_relevant_docs_seen_at_last_rank(self):
    return [query.amount_of_contiguous_non_relevant_documents_seen_at_last_rank() for query in self.queries.values()]

  def cumulated_gain_at(self, seconds_elapsed, gain_levels):
    try:
      cumulated_gain = 0
      for (seconds_at, gain_increment) in self.gain_events(gain_levels):
        if seconds_at > seconds_elapsed:
          return cumulated_gain
        cumulated_gain += gain_increment
      return cumulated_gain
    except RuntimeError as e:
      raise RuntimeError("Cannot calculate cumulated gain at %s secs for session id %s: %s" % (seconds_elapsed, self.record_id, e))

  def gain_events(self, gain_levels):
    possible_gain_actions = self.document_marked_relevant_actions()
    return _memoize_attr(
        self,
        '_gain_events',
        lambda: [self.create_gain_pair(action, gain_levels) for (idx, action) in possible_gain_actions if action.gain(gain_levels) > 0]
    )

  def create_gain_pair(self, action, gain_levels):
    return (self.seconds_elapsed_at(action.timestamp), action.gain(gain_levels))

  def total_snippet_scanning_time_in_seconds(self):
    # No actions -> No scanning time.
    if len(self.actions) == 0:
      return None
    return self.duration_in_seconds() - sum(self.query_formulation_times()) - sum(self.document_read_times().values())

  def cumulated_read_count_at(self, seconds, relevance_level_match=lambda r: True, incidence_match=lambda i: True):
    read_actions = self.document_read_actions_until(seconds)
    return len(list(filter(lambda action: relevance_level_match(action[1].document.get_relevance_for_topic(self.topic).relevance_level) and incidence_match(self.incidence_of(action[1].document, action[1].query)), read_actions)))

  def cumulated_non_relevant_read_count_at(self, seconds):
    read_actions = self.document_read_actions_until(seconds)
    return len(list(filter(lambda action: action[1].document.is_not_relevant_for_topic(self.topic), read_actions)))

  def cumulated_moderately_relevant_read_count_at(self, seconds):
    read_actions = self.document_read_actions_until(seconds)
    return len(list(filter(lambda action: action[1].document.is_moderately_relevant_for_topic(self.topic), read_actions)))

  def cumulated_highly_relevant_read_count_at(self, seconds):
    read_actions = self.document_read_actions_until(seconds)
    return len(list(filter(lambda action: action[1].document.is_highly_relevant_for_topic(self.topic), read_actions)))

  def cumulated_mark_count_at(self, seconds, relevance_level_match=lambda r: True, incidence_match=lambda i: True):
    mark_actions = self.document_marked_relevant_actions_until(seconds)
    return len(list(filter(lambda action: relevance_level_match(action[1].document.get_relevance_for_topic(self.topic).relevance_level) and incidence_match(self.incidence_of(action[1].document, action[1].query)), mark_actions)))

  def cumulated_non_relevant_mark_count_at(self, seconds):
    mark_actions = self.document_marked_relevant_actions_until(seconds)
    return len(list(filter(lambda action: action[1].document.is_not_relevant_for_topic(self.topic), mark_actions)))

  def cumulated_moderately_relevant_mark_count_at(self, seconds):
    mark_actions = self.document_marked_relevant_actions_until(seconds)
    return len(list(filter(lambda action: action[1].document.is_moderately_relevant_for_topic(self.topic), mark_actions)))

  def cumulated_highly_relevant_mark_count_at(self, seconds):
    mark_actions = self.document_marked_relevant_actions_until(seconds)
    return len(list(filter(lambda action: action[1].document.is_highly_relevant_for_topic(self.topic), mark_actions)))

  def results_count_at_rank(self, rank, relevance_level_match=lambda r: True, incidence_match=lambda i: True):
    if rank is None or rank < 1:
      return None
    total_count = 0
    remain = rank
    for query in self.sorted_queries():
      if query.continuous_rank_at_end() < rank:
        total_count += len(list(filter(lambda result_document: incidence_match(self.incidence_of(result_document.document, query)), query.results_of_relevance_level(relevance_level_match))))
        remain -= query.last_rank_reached()
      else:
        total_count += len(list(filter(lambda result_document: incidence_match(self.incidence_of(result_document.document, query)), query.results_up_to_rank(remain, relevance_level_match=relevance_level_match))))
        break
    return total_count

  def non_relevant_results_count_at_rank(self, rank):
    if rank is None or rank < 1:
      return None
    total_count = 0
    remain = rank
    for query in self.sorted_queries():
      if query.continuous_rank_at_end() < rank:
        total_count += len(query.non_relevant_results())
        remain -= query.last_rank_reached()
      else:
        total_count += len(query.non_relevant_results_up_to_rank(remain))
        break
    return total_count

  def moderately_relevant_results_count_at_rank(self, rank):
    if rank is None or rank < 1:
      return None
    total_count = 0
    remain = rank
    for query in self.sorted_queries():
      if query.continuous_rank_at_end() < rank:
        total_count += len(query.moderately_relevant_results())
        remain -= query.last_rank_reached()
      else:
        total_count += len(query.moderately_relevant_results_up_to_rank(remain))
        break
    return total_count

  def highly_relevant_results_count_at_rank(self, rank):
    if rank is None or rank < 1:
      return None
    total_count = 0
    remain = rank
    for query in self.sorted_queries():
      if query.continuous_rank_at_end() < rank:
        total_count += len(query.highly_relevant_results())
        remain -= query.last_rank_reached()
      else:
        total_count += len(query.highly_relevant_results_up_to_rank(remain))
        break
    return total_count

  def document_has_been_marked_relevant_before(self, document, action):
    mark_actions_before_this = self.document_marked_relevant_actions_until(
        self.seconds_elapsed_at(action.timestamp) - 0.001)
    return document.record_id in [action.document.record_id for idx, action in mark_actions_before_this]

  @classmethod
  def average_document_reading_time_in_seconds_over(cls, sessions):
    reading_times = cls.document_reading_times_in_seconds_over(sessions)
    return sum(reading_times) / len(reading_times)

  @classmethod
  def median_document_reading_time_in_seconds_over(cls, sessions):
    reading_times = cls.document_reading_times_in_seconds_over(sessions)
    return numpy.median(reading_times)

  @classmethod
  def std_document_reading_time_in_seconds_over(cls, sessions):
    reading_times = cls.document_reading_times_in_seconds_over(sessions)
    return numpy.std(reading_times)

  @classmethod
  def mean_document_reading_time_in_seconds_over(cls, sessions):
    reading_times = cls.document_reading_times_in_seconds_over(sessions)
    return numpy.mean(reading_times)

  @classmethod
  def document_reading_times_in_seconds_over(cls, sessions):
    reading_times = [session.document_read_times().values() for session in sessions]
    # Remove Nones from the reading times
    return list(filter(None.__ne__, itertools.chain.from_iterable(reading_times)))

  @classmethod
  def average_query_formulation_time_in_seconds_over(cls, sessions):
    querying_durations = cls.query_formulation_times_in_seconds_over(sessions)
    return sum(querying_durations) / len(querying_durations)

  @classmethod
  def median_query_formulation_time_in_seconds_over(cls, sessions):
    querying_durations = cls.query_formulation_times_in_seconds_over(sessions)
    return numpy.median(querying_durations)

  @classmethod
  def std_query_formulation_time_in_seconds_over(cls, sessions):
    querying_durations = cls.query_formulation_times_in_seconds_over(sessions)
    return numpy.std(querying_durations)

  @classmethod
  def query_formulation_times_in_seconds_over(cls, sessions):
    querying_durations = [session.querying_durations() for session in sessions]
    return list(filter(None.__ne__, itertools.chain.from_iterable(querying_durations)))

  @classmethod
  def average_snippet_scanning_time_in_seconds_over(cls, sessions):
    total_snippet_scanning_times = [session.total_snippet_scanning_time_in_seconds() for session in sessions]
    total_snippet_scanning_time = sum(filter(None.__ne__, total_snippet_scanning_times))
    total_seen_documents_amount = sum([len(session.seen_documents) for session in sessions])
    return total_snippet_scanning_time / total_seen_documents_amount

  @classmethod
  def average_last_rank_reached_over(cls, sessions):
    last_ranks = cls.last_ranks_reached_over(sessions)
    return sum(last_ranks) / len(last_ranks)

  @classmethod
  def median_last_rank_reached_over(cls, sessions):
    last_ranks = cls.last_ranks_reached_over(sessions)
    return numpy.median(last_ranks)

  @classmethod
  def std_last_rank_reached_over(cls, sessions):
    last_ranks = cls.last_ranks_reached_over(sessions)
    return numpy.std(last_ranks)

  @classmethod
  def last_ranks_reached_over(cls, sessions):
    last_ranks = [session.last_ranks() for session in sessions]
    return list(filter(None.__ne__, itertools.chain.from_iterable(last_ranks)))

  @classmethod
  def average_amount_of_non_relevant_documents_seen_at_last_rank_over(cls, sessions):
    amounts_of_non_relevant_docs_seen_at_last_rank = cls.amounts_of_non_relevant_documents_seen_at_last_rank_over(sessions)
    return sum(amounts_of_non_relevant_docs_seen_at_last_rank) / len(amounts_of_non_relevant_docs_seen_at_last_rank)

  @classmethod
  def median_amount_of_non_relevant_documents_seen_at_last_rank_over(cls, sessions):
    amounts_of_non_relevant_docs_seen_at_last_rank = cls.amounts_of_non_relevant_documents_seen_at_last_rank_over(sessions)
    return numpy.median(amounts_of_non_relevant_docs_seen_at_last_rank)

  @classmethod
  def std_amount_of_non_relevant_documents_seen_at_last_rank_over(cls, sessions):
    amounts_of_non_relevant_docs_seen_at_last_rank = cls.amounts_of_non_relevant_documents_seen_at_last_rank_over(sessions)
    return numpy.std(amounts_of_non_relevant_docs_seen_at_last_rank)

  @classmethod
  def amounts_of_non_relevant_documents_seen_at_last_rank_over(cls, sessions):
    amounts_of_non_relevant_docs_seen_at_last_rank = [session.amounts_of_non_relevant_docs_seen_at_last_rank() for session in sessions]
    return list(filter(None.__ne__, itertools.chain.from_iterable(amounts_of_non_relevant_docs_seen_at_last_rank)))

  @classmethod
  def average_amount_of_contiguous_non_relevant_documents_seen_at_last_rank_over(cls, sessions):
    amounts_of_contiguous_non_relevant_docs_seen_at_last_rank = cls.amounts_of_contiguous_non_relevant_documents_seen_at_last_rank_over(sessions)
    return sum(amounts_of_contiguous_non_relevant_docs_seen_at_last_rank) / len(amounts_of_contiguous_non_relevant_docs_seen_at_last_rank)

  @classmethod
  def median_amount_of_contiguous_non_relevant_documents_seen_at_last_rank_over(cls, sessions):
    amounts_of_contiguous_non_relevant_docs_seen_at_last_rank = cls.amounts_of_contiguous_non_relevant_documents_seen_at_last_rank_over(sessions)
    return numpy.median(amounts_of_contiguous_non_relevant_docs_seen_at_last_rank)

  @classmethod
  def std_amount_of_contiguous_non_relevant_documents_seen_at_last_rank_over(cls, sessions):
    amounts_of_contiguous_non_relevant_docs_seen_at_last_rank = cls.amounts_of_contiguous_non_relevant_documents_seen_at_last_rank_over(sessions)
    return numpy.std(amounts_of_contiguous_non_relevant_docs_seen_at_last_rank)

  @classmethod
  def amounts_of_contiguous_non_relevant_documents_seen_at_last_rank_over(cls, sessions):
    amounts_of_contiguous_non_relevant_docs_seen_at_last_rank = [session.amounts_of_contiguous_non_relevant_docs_seen_at_last_rank() for session in sessions]
    return list(filter(None.__ne__, itertools.chain.from_iterable(amounts_of_contiguous_non_relevant_docs_seen_at_last_rank)))

  @classmethod
  def average_random_click_probability_over(cls, sessions):
    return cls.average_random_click_probability(records=sessions)

  @classmethod
  def median_random_click_probability_over(cls, sessions):
    return cls.median_random_click_probability(records=sessions)

  @classmethod
  def std_random_click_probability_over(cls, sessions):
    return cls.std_random_click_probability(records=sessions)

  @classmethod
  def average_ratio_of_seen_documents_at_rank_over(cls, rank, sessions):
    return cls.ratio_of_seen_documents_at_rank(rank, records=sessions)

  @classmethod
  def average_total_query_duration_over(cls, sessions):
    total_query_durations = cls.total_query_durations_over(sessions)
    return sum(total_query_durations) / len(total_query_durations)

  @classmethod
  def median_total_query_duration_over(cls, sessions):
    total_query_durations = cls.total_query_durations_over(sessions)
    return numpy.median(total_query_durations)

  @classmethod
  def std_total_query_duration_over(cls, sessions):
    total_query_durations = cls.total_query_durations_over(sessions)
    return numpy.std(total_query_durations)

  @classmethod
  def total_query_durations_over(cls, sessions):
    total_query_durations = [session.total_query_durations() for session in sessions]
    return list(filter(None.__ne__, itertools.chain.from_iterable(total_query_durations)))

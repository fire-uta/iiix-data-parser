import itertools


from has_actions import HasActions
from has_queries import HasQueries
from has_documents import HasDocuments


class ActsAsSession(HasActions, HasQueries, HasDocuments):
  def __init__(self, user, topic, condition):
    HasDocuments.__init__(self)
    HasQueries.__init__(self)
    self.user = user
    self.topic = topic
    self.condition = condition

  def total_snippet_scanning_time_in_seconds(self):
    # No actions -> No scanning time.
    if len(self.actions) == 0:
      return None
    return self.duration_in_seconds() - sum(self.query_formulation_times()) - sum(self.document_read_times().values())

  def average_snippet_scanning_time_in_seconds(self):
    return self.total_snippet_scanning_time_in_seconds() / len(self.seen_documents)

  def average_document_reading_time_in_seconds(self):
    read_times = self.document_read_times()
    return sum(read_times.values()) / len(read_times)

  def average_query_formulation_time_in_seconds(self):
    querying_durations = self.querying_durations()
    return sum(querying_durations) / len(querying_durations)

  def querying_durations(self):
    query_start_actions = self.actions_by_type('QUERY_FOCUS')
    return [self.action_duration_in_seconds_for(idx, action, 'QUERY_ISSUED') for idx, action in query_start_actions]

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
        [self.create_gain_pair(action, gain_levels) for (idx, action) in possible_gain_actions if action.gain(gain_levels) > 0]
    )

  def create_gain_pair(self, action, gain_levels):
    return (self.seconds_elapsed_at(action.timestamp), action.gain(gain_levels))

  @classmethod
  def average_document_reading_time_in_seconds_over(cls, sessions):
    reading_times = [session.document_read_times().values() for session in sessions]
    # Remove Nones from the reading times
    merged_reading_times = list(filter(None.__ne__, itertools.chain.from_iterable(reading_times)))
    return sum(merged_reading_times) / len(merged_reading_times)

  @classmethod
  def average_query_formulation_time_in_seconds_over(cls, sessions):
    querying_durations = [session.querying_durations() for session in sessions]
    merged_durations = list(filter(None.__ne__, itertools.chain.from_iterable(querying_durations)))
    return sum(merged_durations) / len(merged_durations)

  @classmethod
  def average_snippet_scanning_time_in_seconds_over(cls, sessions):
    total_snippet_scanning_times = [session.total_snippet_scanning_time_in_seconds() for session in sessions]
    total_snippet_scanning_time = sum(filter(None.__ne__, total_snippet_scanning_times))
    total_seen_documents_amount = sum([len(session.seen_documents) for session in sessions])
    return total_snippet_scanning_time / total_seen_documents_amount

  @classmethod
  def average_last_rank_reached_over(cls, sessions):
    last_ranks = [session.last_ranks() for session in sessions]
    merged_last_ranks = list(filter(None.__ne__, itertools.chain.from_iterable(last_ranks)))
    return sum(merged_last_ranks) / len(merged_last_ranks)

  @classmethod
  def average_amount_of_non_relevant_documents_seen_at_last_rank_over(cls, sessions):
    amounts_of_non_relevant_docs_seen_at_last_rank = [session.amounts_of_non_relevant_docs_seen_at_last_rank() for session in sessions]
    merged_amounts = list(filter(None.__ne__, itertools.chain.from_iterable(amounts_of_non_relevant_docs_seen_at_last_rank)))
    return sum(merged_amounts) / len(merged_amounts)

  @classmethod
  def average_amount_of_contiguous_non_relevant_documents_seen_at_last_rank_over(cls, sessions):
    amounts_of_contiguous_non_relevant_docs_seen_at_last_rank = [session.amounts_of_contiguous_non_relevant_docs_seen_at_last_rank() for session in sessions]
    merged_amounts = list(filter(None.__ne__, itertools.chain.from_iterable(amounts_of_contiguous_non_relevant_docs_seen_at_last_rank)))
    return sum(merged_amounts) / len(merged_amounts)

  @classmethod
  def average_random_click_probability_over(cls, sessions):
    return cls.average_random_click_probability(records=sessions)

  @classmethod
  def average_ratio_of_seen_documents_at_rank_over(cls, rank, sessions):
    return cls.ratio_of_seen_documents_at_rank(rank, records=sessions)

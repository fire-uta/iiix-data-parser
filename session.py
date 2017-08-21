import itertools


from data_record import DataRecord
from filterable import Filterable
from acts_as_session import ActsAsSession


from attr_utils import _memoize_attr


class Session(DataRecord, Filterable, ActsAsSession):

  def __init__(self, session_id, user, topic, condition):
    DataRecord.__init__(self, session_id)
    ActsAsSession.__init__(self, user, topic, condition)

  def add_query(self, query):
    super().add_query(query)
    query.session = self

  def viewed_documents_count_at(self, seconds):
    read_action_tuples = self.document_read_actions_until(seconds)
    unique_docids = set([action_tuple[1].document_id for action_tuple in read_action_tuples])
    return len(unique_docids)

  def marked_documents_count_at(self, seconds):
    mark_action_tuples = self.document_marked_relevant_actions_until(seconds)
    unique_docids = set([action_tuple[1].document_id for action_tuple in mark_action_tuples])
    return len(unique_docids)

  @classmethod
  def build_session_id(cls, user_id, topic_id):
    return str(user_id) + '-' + str(topic_id)

  @classmethod
  def average_duration_in_seconds(cls, filter_func=Filterable.identity_filter):
    sessions = list(filter(filter_func, cls.get_store().values()))
    return reduce(lambda acc, session: acc + session.duration_in_seconds(), sessions, 0) / len(sessions)

  @classmethod
  def global_average_document_reading_time_in_seconds(cls, filter_func=Filterable.identity_filter):
    sessions = list(filter(filter_func, cls.get_store().values()))
    return cls.average_document_reading_time_in_seconds_over(sessions)

  @classmethod
  def global_average_snippet_scanning_time_in_seconds(cls, filter_func=Filterable.identity_filter):
    sessions = list(filter(filter_func, cls.get_store().values()))
    return cls.average_snippet_scanning_time_in_seconds_over(sessions)

  @classmethod
  def average_cumulated_gain_at(cls, seconds_elapsed, gain_levels, filter_func=Filterable.identity_filter):
    sessions = list(filter(filter_func, cls.get_store().values()))
    return reduce(lambda acc, session: acc + float(session.cumulated_gain_at(seconds_elapsed, gain_levels)), sessions, 0.0) / float(len(sessions))

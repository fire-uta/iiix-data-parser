import itertools


from data_record import DataRecord
from has_actions import HasActions
from filterable import Filterable
from has_documents import HasDocuments


class Session(DataRecord, HasActions, Filterable, HasDocuments):

  def __init__(self, session_id, user, topic, condition):
    DataRecord.__init__( self, session_id )
    self.topic = topic
    self.user = user
    self.condition = condition

    self.queries = {}

  def add_query(self, query):
    self.queries[query.record_id] = query
    query.session = self

  def duration_in_seconds(self):
    first_timestamp = self.actions[0].timestamp
    last_timestamp = self.actions[-1].timestamp
    delta = last_timestamp - first_timestamp
    return delta.total_seconds()

  def total_snippet_scanning_time_in_seconds(self):
    return self.duration_in_seconds() - sum(self.query_formulation_times()) - sum(self.document_read_times().values())

  def average_snippet_scanning_time_in_seconds(self):
    return self.total_snippet_scanning_time_in_seconds()/len(self.seen_documents)

  def query_formulation_times(self):
    return [query.formulation_time_in_seconds() for query in self.queries.values()]

  def document_read_actions(self):
    return self.actions_by_type( 'DOC_MARKED_VIEWED' )

  def document_read_times(self):
    read_actions = self.document_read_actions()
    read_times = {}
    for idx, action in read_actions:
      action_duration = self.action_duration_in_seconds_for( idx, action )
      document = action.document
      if read_times.has_key( document.record_id ):
        read_times[ document.record_id ] += action_duration
      else:
        read_times[ document.record_id ] = action_duration
    return read_times

  def average_document_reading_time_in_seconds(self):
    read_times = self.document_read_times()
    return sum(read_times.values()) / len(read_times)

  def average_query_formulation_time_in_seconds(self):
    query_start_actions = self.actions_by_type( 'QUERY_FOCUS' )
    querying_durations = [self.action_duration_in_seconds_for( idx, action, 'QUERY_ISSUED' ) for idx, action in query_start_actions]
    return sum(querying_durations) / len(querying_durations)

  @classmethod
  def build_session_id( cls, user_id, topic_id ):
    return str( user_id ) + '-' + str( topic_id )

  @classmethod
  def average_duration_in_seconds(cls, filter_func = Filterable.identity_filter):
    sessions = filter( filter_func, cls.get_store().values() )
    return reduce( lambda acc, session: acc + session.duration_in_seconds(), sessions, 0 ) / len(sessions)

  @classmethod
  def global_average_document_reading_time_in_seconds(cls, filter_func = Filterable.identity_filter):
    sessions = filter( filter_func, cls.get_store().values() )
    reading_times = [session.document_read_times().values() for session in sessions]
    merged_reading_times = list(itertools.chain.from_iterable( reading_times ))
    return sum(merged_reading_times)/len(merged_reading_times)

  @classmethod
  def global_average_snippet_scanning_time_in_seconds(cls, filter_func = Filterable.identity_filter):
    sessions = filter( filter_func, cls.get_store().values() )
    total_snippet_scanning_time = sum([session.total_snippet_scanning_time_in_seconds() for session in sessions])
    total_seen_documents_amount = sum([len(session.seen_documents) for session in sessions])
    return total_snippet_scanning_time/total_seen_documents_amount

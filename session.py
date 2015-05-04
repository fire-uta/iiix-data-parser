from data_record import DataRecord


class Session(DataRecord):

  no_delays_filter = lambda session: session.condition.record_id == str(6)
  query_delay_filter = lambda session: session.condition.record_id == str(7)
  document_delay_filter = lambda session: session.condition.record_id == str(8)
  combined_delay_filter = lambda session: session.condition.record_id == str(9)

  identity_filter = lambda session: True

  @staticmethod
  def combine_filters( *filters ):
    return lambda session: all([fil( session ) for fil in filters])

  def __init__(self, session_id, user, topic, condition):
    DataRecord.__init__( self, session_id )
    self.topic = topic
    self.user = user
    self.condition = condition

    self.seen_documents = {}
    self.viewed_documents = {}
    self.marked_relevant_documents = {}

  def add_seen_documents(self, *documents):
    for document in documents:
      self.seen_documents[ document.record_id ] = document

  def add_viewed_documents( self, *documents ):
    for document in documents:
      self.viewed_documents[ document.record_id ] = document

  def add_marked_relevant_documents( self, *documents ):
    for document in documents:
      self.marked_relevant_documents[ document.record_id ] = document

  def seen_highly_relevant_documents(self):
    return [document for document in self.seen_documents.values() if document.is_highly_relevant_for_topic( self.topic )]

  def seen_moderately_relevant_documents(self):
    return [document for document in self.seen_documents.values() if document.is_moderately_relevant_for_topic( self.topic )]

  def seen_non_relevant_documents(self):
    return [document for document in self.seen_documents.values() if not document.is_relevant_for_topic( self.topic )]

  def viewed_highly_relevant_documents(self):
    return [document for document in self.viewed_documents.values() if document.is_highly_relevant_for_topic( self.topic )]

  def viewed_moderately_relevant_documents(self):
    return [document for document in self.viewed_documents.values() if document.is_moderately_relevant_for_topic( self.topic )]

  def viewed_non_relevant_documents(self):
    return [document for document in self.viewed_documents.values() if not document.is_relevant_for_topic( self.topic )]

  @classmethod
  def build_session_id( cls, user_id, topic_id ):
    return str( user_id ) + '-' + str( topic_id )

  @classmethod
  def amount_of_seen_highly_relevant_documents(cls, filter_func = identity_filter):
    sessions = cls.get_store().values()
    return reduce( lambda acc, session: acc + len(session.seen_highly_relevant_documents()), filter(filter_func, sessions), 0 )

  @classmethod
  def amount_of_viewed_highly_relevant_documents(cls, filter_func = identity_filter):
    sessions = cls.get_store().values()
    return reduce( lambda acc, session: acc + len(session.viewed_highly_relevant_documents()), filter(filter_func, sessions), 0 )

  @classmethod
  def amount_of_seen_moderately_relevant_documents(cls, filter_func = identity_filter):
    sessions = cls.get_store().values()
    return reduce( lambda acc, session: acc + len(session.seen_moderately_relevant_documents()), filter(filter_func, sessions), 0 )

  @classmethod
  def amount_of_viewed_moderately_relevant_documents(cls, filter_func = identity_filter):
    sessions = cls.get_store().values()
    return reduce( lambda acc, session: acc + len(session.viewed_moderately_relevant_documents()), filter(filter_func, sessions), 0 )

  @classmethod
  def amount_of_seen_non_relevant_documents(cls, filter_func = identity_filter):
    sessions = cls.get_store().values()
    return reduce( lambda acc, session: acc + len(session.seen_non_relevant_documents()), filter(filter_func, sessions), 0 )

  @classmethod
  def amount_of_viewed_non_relevant_documents(cls, filter_func = identity_filter):
    sessions = cls.get_store().values()
    return reduce( lambda acc, session: acc + len(session.viewed_non_relevant_documents()), filter(filter_func, sessions), 0 )

from data_record import DataRecord


class Session(DataRecord):
  def __init__(self, session_id, user, topic):
    DataRecord.__init__( self, session_id )
    self.topic = topic
    self.user = user

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

  @classmethod
  def build_session_id( cls, user_id, topic_id ):
    return str( user_id ) + '-' + str( topic_id )

  @classmethod
  def amount_of_seen_highly_relevant_documents(cls):
    sessions = cls.get_store().values()
    return reduce( lambda acc, session: acc + len(session.seen_highly_relevant_documents()), sessions, 0 )

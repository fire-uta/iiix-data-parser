from data_record import DataRecord


class Session(DataRecord):
  def __init__(self, session_id, user, topic):
    DataRecord.__init__( self, session_id )
    self.topic = topic
    self.user = user

  @classmethod
  def build_session_id( cls, user_id, topic_id ):
    return str( user_id ) + '-' + str( topic_id )

from data_record import DataRecord


class User(DataRecord):
  def __init__(self, user_id):
    DataRecord.__init__( self, user_id )

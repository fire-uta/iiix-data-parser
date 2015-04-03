from data_record import DataRecord
from has_actions import HasActions


class User(DataRecord, HasActions):
  def __init__(self, user_id):
    DataRecord.__init__( self, user_id )

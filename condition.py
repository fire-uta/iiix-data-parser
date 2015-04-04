from numpy import uint8


from data_record import DataRecord


class Condition(DataRecord):
  def __init__(self, condition_id):
    DataRecord.__init__( self, uint8(condition_id) )

from data_record import DataRecord


class Document(DataRecord):
  def __init__(self, docid):
    DataRecord.__init__( self, docid )

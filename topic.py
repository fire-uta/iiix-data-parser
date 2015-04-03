from relevance import Relevance
from data_record import DataRecord


class Topic(DataRecord):
  def __init__(self, topic_identifier):
    DataRecord.__init__( self, topic_identifier )
    self.relevances = []

  def add_relevance( self, document, relevance_level ):
    self.relevances.append( Relevance( self, document, relevance_level ) )

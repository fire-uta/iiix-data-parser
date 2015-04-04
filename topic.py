from numpy import uint16


from relevance import Relevance
from data_record import DataRecord
from has_actions import HasActions


class Topic(DataRecord, HasActions):
  def __init__(self, topic_identifier):
    DataRecord.__init__( self, uint16(topic_identifier) )
    self.relevances = []

  def add_relevance( self, document, relevance_level ):
    self.relevances.append( Relevance( self, document, relevance_level ) )

from numpy import uint16
from numpy import bool_


from query_result_list import QueryResultList
from data_record import DataRecord
from has_actions import HasActions


class Query(DataRecord, HasActions):
  def __init__(self, query_id, topic = None, result_list = None, user = None, condition = None, autocomplete = None, query_text = None):
    DataRecord.__init__( self, uint16(query_id) )
    self.topic = topic
    self.result_list = result_list
    self.user = user
    self.condition = condition
    self.autocomplete = bool_(autocomplete)
    self.query_text = query_text
    if result_list is None: self.result_list = QueryResultList(self)

  def add_to_result_list( self, rank, document ):
    self.result_list.add( rank, document )

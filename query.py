from numpy import uint16
from numpy import bool_


from query_result_list import QueryResultList
from data_record import DataRecord
from has_actions import HasActions


class Query(DataRecord, HasActions):
  def __init__(self, query_id, topic = None, user = None, condition = None, autocomplete = None, query_text = None):
    DataRecord.__init__( self, uint16(query_id) )
    self.topic = topic
    self.user = user
    self.condition = condition
    self.autocomplete = bool_(autocomplete)
    self.query_text = query_text
    self.result_list = QueryResultList(self)

  def add_to_result_list( self, rank, document ):
    self.result_list.add( rank, document )

  def results_up_to_rank( self, rank ):
    if int(rank) < 1 or int(rank) > self.result_list.length():
        raise RuntimeError("Attempted to fetch results up to rank %s for query %s, which is impossible." % (rank, self.record_id))
    return self.result_list.results_up_to_rank( rank )

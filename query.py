from numpy import uint16
from numpy import bool_


from query_result_list import QueryResultList
from data_record import DataRecord
from has_actions import HasActions
from session import Session
from filterable import Filterable
from has_documents import HasDocuments


class Query(DataRecord, HasActions, Filterable, HasDocuments):
  def __init__(self, query_id, topic = None, user = None, condition = None, autocomplete = None, query_text = None, session = None):
    DataRecord.__init__( self, uint16(query_id) )
    HasDocuments.__init__( self )
    self.topic = topic
    self.user = user
    self.condition = condition
    self.autocomplete = bool_(autocomplete)
    self.query_text = query_text
    self.session = session
    self.result_list = QueryResultList(self)

  def add_to_result_list( self, rank, document ):
    self.result_list.add( rank, document )

  def results_up_to_rank( self, rank ):
    if int(rank) < 1 or int(rank) > self.result_list.length():
        raise RuntimeError("Attempted to fetch results up to rank %s for query %s, which is impossible." % (rank, self.record_id))
    return self.result_list.results_up_to_rank( rank )

  def formulation_time_in_seconds(self):
    (idx, query_start_action) = self.actions_by_type( 'QUERY_FOCUS' )[0]
    return self.action_duration_in_seconds_for( idx, query_start_action, 'QUERY_ISSUED' )

  def last_rank_reached(self):
    for action in reversed(self.actions):
      if hasattr( action, 'rank' ):
        return int(action.rank)
    # No actions with ranks. Likely bailed before reading anything. Counts as rank 1.
    return 1

  @classmethod
  def average_formulation_time_in_seconds(cls, filter_func = lambda query: True):
    queries = filter( filter_func, cls.get_store().values() )
    return reduce( lambda acc, query: acc + query.formulation_time_in_seconds(), queries, 0 ) / len(queries)

  @classmethod
  def average_last_rank_reached(cls, filter_func = lambda query: True):
    queries = filter( filter_func, cls.get_store().values() )
    return reduce( lambda acc, query: acc + float(query.last_rank_reached()), queries, 0.0 ) / float(len(queries))

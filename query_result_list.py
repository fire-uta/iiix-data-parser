from query_result_document import QueryResultDocument


class QueryResultList:
  def __init__(self, query):
    self.result_documents = [] # Guaranteed to be in rank order
    self.query = query

  def add( self, rank, document ):
    self.result_documents.insert( int(rank) - 1, QueryResultDocument( self, rank, document ) )

  def results_up_to_rank( self, rank ):
    return self.result_documents[:int(rank)]

  def results_between(self, rank_start, rank_end):
    return self.result_documents[(int(rank_start) - 1):int(rank_end)]

  def length( self ):
    return len( self.result_documents )

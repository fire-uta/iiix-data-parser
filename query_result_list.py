from query_result_document import QueryResultDocument


class QueryResultList:
  def __init__(self, query, result_documents = []):
    self.result_documents = result_documents # Guaranteed to be in rank order
    self.query = query

  def add( self, rank, document ):
    self.result_documents.insert( int(rank) - 1, QueryResultDocument( self, rank, document ) )

  def results_up_to_rank( self, rank ):
    return self.result_documents[:int(rank)]

from query_result_document import QueryResultDocument


class QueryResultList:
  def __init__(self, query, result_documents = []):
    self.result_documents = result_documents
    self.query = query

  def add( self, rank, document ):
    self.result_documents.append( QueryResultDocument( self, rank, document ) )

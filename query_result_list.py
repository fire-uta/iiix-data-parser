from query_result_document import QueryResultDocument

from attr_utils import _memoize_attr


class QueryResultList:
  def __init__(self, query):
    self.result_documents = [] # Guaranteed to be in rank order
    self.query = query

  def add( self, rank, document ):
    self.result_documents.insert( int(rank) - 1, QueryResultDocument( self, rank, document ) )

  def results_up_to_rank(self, rank, relevance_level_match=lambda r: True):
    return filter(lambda result_document: relevance_level_match(result_document.get_relevance_for_topic(self.query.topic).relevance_level), self.result_documents[:int(rank)])

  def non_relevant_results_up_to_rank(self, rank):
    return _memoize_attr(
        self,
        '_non_relevant_results_up_to_rank_' + str(rank),
        lambda: list(filter(lambda result_document: result_document.is_not_relevant_for_topic(self.query.topic), self.result_documents[:int(rank)]))
    )

  def moderately_relevant_results_up_to_rank(self, rank):
    return _memoize_attr(
        self,
        '_moderately_relevant_results_up_to_rank_' + str(rank),
        lambda: list(filter(lambda result_document: result_document.is_moderately_relevant_for_topic(self.query.topic), self.result_documents[:int(rank)]))
    )

  def highly_relevant_results_up_to_rank(self, rank):
    return _memoize_attr(
        self,
        '_highly_relevant_results_up_to_rank_' + str(rank),
        lambda: list(filter(lambda result_document: result_document.is_highly_relevant_for_topic(self.query.topic), self.result_documents[:int(rank)]))
    )

  def results_between(self, rank_start, rank_end):
    return self.result_documents[(int(rank_start) - 1):int(rank_end)]

  def length(self):
    return len(self.result_documents)

  def results_up_to_last_rank_reached(self):
    return self.results_up_to_rank(self.query.last_rank_reached())

  def result_document_first_encountered_at_from_session_start_seconds(self, result_document):
    for action in self.query.actions:
      if hasattr(action, 'document_id') and action.document_id == result_document.document.record_id:
        query_start_seconds = self.query.session.seconds_elapsed_at(self.query.get_start_timestamp())
        return query_start_seconds + self.query.seconds_elapsed_at(action.timestamp)
    return None

  def result_document_read_start_at_from_session_start_seconds(self, result_document):
    if not self.query.has_been_viewed(result_document.document):
      return None
    query_start_seconds = self.query.session.seconds_elapsed_at(self.query.get_start_timestamp())
    read_at_from_query_start = self.query.document_read_start_at_seconds(result_document.document)
    return query_start_seconds + read_at_from_query_start

  def result_document_mark_start_at_from_session_start_seconds(self, result_document):
    if not self.query.has_been_marked(result_document.document):
      return None
    query_start_seconds = self.query.session.seconds_elapsed_at(self.query.get_start_timestamp())
    mark_at_from_query_start = self.query.document_mark_start_at_seconds(result_document.document)
    return query_start_seconds + mark_at_from_query_start

  def rank_of(self, document):
    return _memoize_attr(
        self,
        '_rank_of_' + str(document.record_id),
        lambda: self._calculate_rank_of(document)
    )

  def _calculate_rank_of(self, document):
    for result_document in self.result_documents:
      if result_document.document.record_id == document.record_id:
        return result_document.rank
    return None

  def result_document_clicked(self, result_document):
    # NOTE: assumes that a document can only exist once in a result list
    return self.query.has_been_viewed(result_document.document)

  def result_document_marked(self, result_document):
    # NOTE: assumes that a document can only exist once in a result list
    return self.query.has_been_marked(result_document.document)

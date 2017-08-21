from numpy import uint16


class QueryResultDocument:
  def __init__(self, result_list, rank, document):
    self.result_list = result_list
    self.rank = uint16(rank)
    self.document = document

  def is_relevant_for_topic(self, topic):
    return self.document.is_relevant_for_topic(topic)

  def is_not_relevant_for_topic(self, topic):
    return self.document.is_not_relevant_for_topic(topic)

  def is_moderately_relevant_for_topic(self, topic):
    return self.document.is_moderately_relevant_for_topic(topic)

  def is_highly_relevant_for_topic(self, topic):
    return self.document.is_highly_relevant_for_topic(topic)

  def first_encountered_at_from_session_start_seconds(self):
    return self.result_list.result_document_first_encountered_at_from_session_start_seconds(self)

  def read_start_at_from_session_start_seconds(self):
    return self.result_list.result_document_read_start_at_from_session_start_seconds(self)

  def mark_start_at_from_session_start_seconds(self):
    return self.result_list.result_document_mark_start_at_from_session_start_seconds(self)

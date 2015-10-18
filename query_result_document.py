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

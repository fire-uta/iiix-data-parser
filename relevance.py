from numpy import uint8


class Relevance:
  def __init__(self, topic, document, relevance_level):
    self.topic = topic
    self.document = document
    self.relevance_level = uint8(relevance_level)

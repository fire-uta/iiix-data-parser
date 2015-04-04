from numpy import uint8


class Relevance:
  def __init__(self, topic, document, relevance_level):
    self.topic = topic
    self.document = document
    self.relevance_level = uint8(relevance_level)
    self.document.add_relevance( self )

  def is_relevant(self):
    return self.relevance_level > 0

  def is_highly_relevant(self):
    return self.relevance_level == 2

  def is_moderately_relevant(self):
    return self.relevance_level == 1

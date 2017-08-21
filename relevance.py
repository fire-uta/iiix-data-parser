from data_record import DataRecord

from numpy import uint8

from attr_utils import _memoize_attr


class Relevance(DataRecord):
  def __init__(self, topic, document, relevance_level):
    DataRecord.__init__(self, topic.record_id + '-' + document.record_id)
    self.topic = topic
    self.document = document
    self.relevance_level = uint8(relevance_level)
    self.document.add_relevance( self )

  def is_relevant(self):
    return _memoize_attr(
        self,
        '_is_relevant',
        lambda: self.relevance_level > 0
    )

  def is_highly_relevant(self):
    return _memoize_attr(
        self,
        '_is_highly_relevant',
        lambda: self.relevance_level == 2
    )

  def is_moderately_relevant(self):
    return _memoize_attr(
        self,
        '_is_moderately_relevant',
        lambda: self.relevance_level == 1
    )

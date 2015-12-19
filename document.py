import sys


from numpy import uint16


from data_record import DataRecord


class Document(DataRecord):
  def __init__(self, docid):
    DataRecord.__init__( self, docid )
    self.relevances = {}

  def add_relevance(self, relevance):
    self.relevances[ str(relevance.topic.record_id) ] = relevance

  def get_relevance_for_topic(self, topic):
    return self.get_relevance_for_topic_id( topic.record_id )

  def get_relevance_for_topic_id(self, topic_id):
    return self.relevances.get( str(topic_id) )

  def is_relevant_for_topic(self, topic):
    return self.is_relevant_for_topic_id( topic.record_id )

  def is_not_relevant_for_topic(self, topic):
    return not self.is_relevant_for_topic( topic )

  def is_relevant_for_topic_id(self, topic_id):
    return self.get_relevance_for_topic_id( topic_id ).is_relevant()

  def is_highly_relevant_for_topic(self, topic):
    return self.is_highly_relevant_for_topic_id( topic.record_id )

  def is_highly_relevant_for_topic_id(self, topic_id):
    relevance = self.get_relevance_for_topic_id( topic_id )
    if relevance is None:
      raise RuntimeError( "ERROR: No relevance data found for document %s, topic %s. Available for topics: %s\n" % (self.record_id, topic_id, self.relevances.keys()) )
    return relevance.is_highly_relevant()

  def is_moderately_relevant_for_topic(self, topic):
    return self.is_moderately_relevant_for_topic_id( topic.record_id )

  def is_moderately_relevant_for_topic_id(self, topic_id):
    try:
      return self.get_relevance_for_topic_id( topic_id ).is_moderately_relevant()
    except AttributeError:
      raise RuntimeError("No relevance info found for doc id %s, topic id %s, available rels: %s" % (self.record_id, topic_id, repr(self.relevances)))

from numpy import uint16


from data_record import DataRecord


class Document(DataRecord):
  def __init__(self, docid):
    DataRecord.__init__( self, docid )
    self.relevances = {}

  def add_relevance(self, relevance):
    self.relevances[ relevance.topic.record_id ] = relevance

  def get_relevance_for_topic(self, topic):
    return self.get_relevance_for_topic_id( topic.record_id )

  def get_relevance_for_topic_id(self, topic_id):
    return self.relevances.get( uint16(topic_id) )

  def is_relevant_for_topic(self, topic):
    return self.is_relevant_for_topic_id( topic.record_id )

  def is_relevant_for_topic_id(self, topic_id):
    return self.get_relevance_for_topic_id( topic_id ).is_relevant()

  def is_highly_relevant_for_topic(self, topic):
    return self.is_highly_relevant_for_topic_id( topic.record_id )

  def is_highly_relevant_for_topic_id(self, topic_id):
    return self.get_relevance_for_topic_id( topic_id ).is_highly_relevant()

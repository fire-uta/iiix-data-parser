class Filterable:
  no_delays_filter = lambda filterable: filterable.condition.record_id == str(6)
  query_delay_filter = lambda filterable: filterable.condition.record_id == str(7)
  document_delay_filter = lambda filterable: filterable.condition.record_id == str(8)
  combined_delay_filter = lambda filterable: filterable.condition.record_id == str(9)

  practice_topic_reject_filter = lambda filterable: filterable.topic.record_id != str(367)

  @staticmethod
  def topic_filter( topic_id ):
    return lambda filterable: filterable.topic.record_id == str( topic_id )

  highly_relevant_filter = lambda filterable: filterable.document.is_highly_relevant_for_topic( filterable.topic )
  moderately_relevant_filter = lambda filterable: filterable.document.is_moderately_relevant_for_topic( filterable.topic )
  relevant_filter = lambda filterable: filterable.document.is_relevant_for_topic( filterable.topic )

  identity_filter = lambda filterable: True

  @staticmethod
  def combine_filters( *filters ):
    return lambda filterable: all([fil( filterable ) for fil in filters])

  @classmethod
  def filtered_records(cls, filter_func):
    return filter( filter_func, cls.get_store().values() )

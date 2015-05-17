class Filterable:
  no_delays_filter = lambda filterable: filterable.condition.record_id == str(6)
  query_delay_filter = lambda filterable: filterable.condition.record_id == str(7)
  document_delay_filter = lambda filterable: filterable.condition.record_id == str(8)
  combined_delay_filter = lambda filterable: filterable.condition.record_id == str(9)

  practice_topic_reject_filter = lambda filterable: filterable.topic.record_id != str(367)

  identity_filter = lambda filterable: True

  @staticmethod
  def combine_filters( *filters ):
    return lambda filterable: all([fil( filterable ) for fil in filters])

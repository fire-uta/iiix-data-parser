from document import Document


class Action:

  highly_relevant_filter = lambda action: action.document_is_highly_relevant()
  moderately_relevant_filter = lambda action: action.document_is_moderately_relevant()
  relevant_filter = lambda action: action.document_is_relevant()

  no_delays_filter = lambda action: action.condition.record_id == 6
  query_delay_filter = lambda action: action.condition.record_id == 7
  document_delay_filter = lambda action: action.condition.record_id == 8
  combined_delay_filter = lambda action: action.condition.record_id == 9

  @staticmethod
  def combine_filters( *filters ):
    return lambda action: all([fil( action ) for fil in filters])

  DOCUMENT_EVENT_PARAMS = [ 'document_id2', 'document_id', 'document_id3', 'user_relevance_score', 'rank' ]
  QUERY_EVENT_PARAMS = [ 'query_id', 'query_text' ]

  PARAMS = {
    'QUERY_ISSUED': QUERY_EVENT_PARAMS,
    'VIEW_SEARCH_RESULTS_PAGE': [ 'result_page' ],
    'DOCUMENT_HOVER_IN': DOCUMENT_EVENT_PARAMS,
    'DOCUMENT_HOVER_OUT': DOCUMENT_EVENT_PARAMS,
    'DOC_MARKED_VIEWED': DOCUMENT_EVENT_PARAMS,
    'DOC_MARKED_RELEVANT': DOCUMENT_EVENT_PARAMS,
    'QUERY_FOCUS': [],
    'NEXT_QUERY_ISSUED': QUERY_EVENT_PARAMS,
    'NEXT_QUERY_FOCUS': [],
    'INTERACTION_COMPLETE': [],
    'EXPERIMENT_TIMEOUT': [],
    'SEARCH_TASK_COMPLETED': []
  }

  type_dict = {}

  @classmethod
  def __index_by_type( cls, action ):
    if not action.action_type in cls.type_dict:
      cls.type_dict[ action.action_type ] = []
    cls.type_dict[ action.action_type ].append( action )

  @classmethod
  def by_type( cls, type ):
    return cls.type_dict.get( type )

  @classmethod
  def filter_by_type( cls, type, filter_func ):
    actions_by_type = cls.by_type( type )
    return filter( filter_func, actions_by_type )

  def __init__(self, timestamp, user, condition, topic, action_type, action_parameters):
    self.timestamp = timestamp
    self.user = user
    self.condition = condition
    self.topic = topic
    self.action_type = action_type
    self.bare_action_parameters = action_parameters
    self.__parse_action_parameters()
    self.__index()

  def __parse_action_parameters(self):
    params_list = str(self.bare_action_parameters).split(' ')
    params_order = Action.PARAMS[ self.action_type ]
    for param_name, param_value in zip(params_order, params_list):
      setattr(self, param_name, param_value)
    self.__init_action_parameter_objects()

  def __init_action_parameter_objects(self):
    if hasattr(self, 'document_id'):
      self.document = Document.create_or_update( self.document_id )

  def __index( self ):
    self.__class__.__index_by_type( self )

  def document_is_highly_relevant( self ):
    return self.document.is_highly_relevant_for_topic( self.topic )

  def document_is_moderately_relevant( self ):
    return self.document.is_moderately_relevant_for_topic( self.topic )

  def document_is_relevant( self ):
    return self.document.is_relevant_for_topic( self.topic )

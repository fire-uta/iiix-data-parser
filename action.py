class Action:

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
  def index_by_type( cls, action ):
    if not action.action_type in cls.type_dict:
      cls.type_dict[ action.action_type ] = []
    cls.type_dict[ action.action_type ].append( action )

  @classmethod
  def by_type( cls, type ):
    return cls.type_dict.get( type )

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
    self.action_parameters = dict(zip(params_order, params_list))

  def __index( self ):
    self.__class__.index_by_type( self )

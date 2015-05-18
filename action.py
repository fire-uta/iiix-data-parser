from document import Document
from filterable import Filterable


class Action(Filterable):

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

  global_highest_rank = 0

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

  def __init__(self, timestamp, condition, session, action_type, query, action_parameters):
    self.timestamp = timestamp
    self.session = session
    self.topic = self.session.topic
    self.condition = condition
    self.action_type = action_type
    self.query = query
    self.bare_action_parameters = action_parameters
    self.__parse_action_parameters()
    self.__update_session()
    self.__update_global_stats()
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

  def __update_session( self ):
    if self.action_type == 'DOC_MARKED_VIEWED':
      self.session.add_viewed_documents( self.document )

      # FIXME: THIS IS A HACK BECAUSE RANK CAN SOMETIMES BE UNKNOWN, AND IS MARKED WITH -1
      if int(self.rank) > 0:
        seen_results = self.query.results_up_to_rank( self.rank )
        self.session.add_seen_documents( *[result.document for result in seen_results] )
      else:
        self.session.add_seen_documents( self.document )

    elif self.action_type == 'DOC_MARKED_RELEVANT':
      self.session.add_marked_relevant_documents( self.document )

  def __update_global_stats( self ):
    if hasattr( self, 'rank' ) and int(self.rank) > Action.global_highest_rank:
      Action.global_highest_rank = int(self.rank)

  def document_is_highly_relevant( self ):
    return self.document.is_highly_relevant_for_topic( self.session.topic )

  def document_is_moderately_relevant( self ):
    return self.document.is_moderately_relevant_for_topic( self.session.topic )

  def document_is_relevant( self ):
    return self.document.is_relevant_for_topic( self.session.topic )

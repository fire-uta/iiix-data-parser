from data_record import DataRecord
from document import Document
from filterable import Filterable
from cli import CLI
import parser


def get_cli_options():
  (options, args) = CLI.parsedArgs
  return options


def should_use_alt_params():
  return get_cli_options().use_alt_log_format


def serp_len():
  return parser.serp_len()


class Action(DataRecord, Filterable):

  READ_ACTION_NAME = 'DOC_MARKED_VIEWED'
  MARK_ACTION_NAME = 'DOC_MARKED_RELEVANT'
  SERP_SWITCH_ACTION_NAME = 'VIEW_SEARCH_RESULTS_PAGE'

  DOCUMENT_EVENT_PARAMS = ['document_id2', 'document_id', 'document_id3', 'user_relevance_score', 'rank']
  ALT_DOCUMENT_EVENT_PARAMS = ['document_id2', 'document_id', 'user_relevance_score', 'rank']
  QUERY_EVENT_PARAMS = ['query_id', 'query_text']
  ALT_QUERY_EVENT_PARAMS = ['query_text']

  PARAMS = {
      'QUERY_ISSUED': QUERY_EVENT_PARAMS,
      'DOCUMENT_HOVER_IN': DOCUMENT_EVENT_PARAMS,
      'DOCUMENT_HOVER_OUT': DOCUMENT_EVENT_PARAMS,
      'QUERY_FOCUS': [],
      'NEXT_QUERY_ISSUED': QUERY_EVENT_PARAMS,
      'NEXT_QUERY_FOCUS': [],
      'INTERACTION_COMPLETE': [],
      'EXPERIMENT_TIMEOUT': [],
      'SEARCH_TASK_COMPLETED': []
  }
  PARAMS[READ_ACTION_NAME] = DOCUMENT_EVENT_PARAMS
  PARAMS[MARK_ACTION_NAME] = DOCUMENT_EVENT_PARAMS
  PARAMS[SERP_SWITCH_ACTION_NAME] = ['result_page']

  ALT_PARAMS = PARAMS.copy()
  ALT_PARAMS[READ_ACTION_NAME] = ALT_DOCUMENT_EVENT_PARAMS
  ALT_PARAMS.update({
      'DEMOGRAPHICS_SURVEY_STARTED': [],
      'DEMOGRAPHICS_SURVEY_COMPLETED': [],
      'SELF_SEARCH_EFFICACY_SURVEY_STARTED': [],
      'SELF_SEARCH_EFFICACY_SURVEY_COMPLETED': [],
      'PRE_TASK_SURVEY_COMPLETED': [],
      'SEARCH_TASK_COMMENCED': [],
      'VIEW_SEARCH_BOX': [],
      'SEARCH_TASK_VIEWED': [],
      'VIEW_SAVED_DOCS': [],
      'POST_TASK_SURVEY_COMPLETED': [],
      'NASA_LOAD_SURVEY_STARTED': [],
      'NASA_LOAD_SURVEY_COMPLETED': [],
      'NASA_QUERY_LOAD_SURVEY_STARTED': [],
      'NASA_QUERY_LOAD_SURVEY_COMPLETED': [],
      'NASA_NAVIGATION_LOAD_SURVEY_STARTED': [],
      'NASA_NAVIGATION_LOAD_SURVEY_COMPLETED': [],
      'NASA_ASSESSMENT_LOAD_SURVEY_STARTED': [],
      'NASA_ASSESSMENT_LOAD_SURVEY_COMPLETED': [],
      'NASA_COMPARE_FACTORS_SURVEY_STARTED': [],
      'NASA_COMPARE_FACTORS_SURVEY_COMPLETED': [],
      'PERFORMANCE': [],
      'DOC_MARKED_NONRELEVANT': DOCUMENT_EVENT_PARAMS,
      'QUERY_SUGGESTION_ISSUED': ALT_QUERY_EVENT_PARAMS,
      'QUERY_ISSUED': ALT_QUERY_EVENT_PARAMS
  })

  CSV_EXPORT_FIELDS = ['record_id', 'timestamp', 'session', 'topic', 'condition', 'action_type', 'query', 'result_page',
                       'document', 'rank', 'user_relevance_score']

  type_dict = {}

  global_highest_rank = 0

  @classmethod
  def __index_by_type(cls, action):
    if action.action_type not in cls.type_dict:
      cls.type_dict[action.action_type] = []
    cls.type_dict[action.action_type].append(action)

  @classmethod
  def by_type(cls, type):
    return cls.type_dict.get(type)

  @classmethod
  def filter_by_type( cls, type, filter_func ):
    actions_by_type = cls.by_type( type )
    return list(filter( filter_func, actions_by_type ))

  def __init__(self, timestamp, condition, session, action_type, query, action_parameters, serp_page_num=None):
    DataRecord.__init__(self, session.record_id + '-' + str(timestamp))
    self.timestamp = timestamp
    self.session = session
    self.topic = self.session.topic
    self.condition = condition
    self.action_type = action_type
    self.query = query
    self.bare_action_parameters = action_parameters
    self.serp_page_num = serp_page_num
    self.__parse_action_parameters()
    self.__update_session()
    self.__update_global_stats()
    self.__index()

  def __parse_action_parameters(self):
    params_list = str(self.bare_action_parameters).split(' ')

    params_order = []
    if should_use_alt_params():
      params_order = Action.ALT_PARAMS[ self.action_type ]
    else:
      params_order = Action.PARAMS[ self.action_type ]

    for param_name, param_value in zip(params_order, params_list):
      setattr(self, param_name, param_value)
    self.__init_action_parameter_objects()

    if self.is_serp_switch_event():
      self.serp_page_num = self.result_page

  def __init_action_parameter_objects(self):
    if hasattr(self, 'document_id'):
      self.document = Document.create_or_update( self.document_id )

  def __index( self ):
    self.__class__.__index_by_type( self )

  def __update_session(self):
    if self.is_read_event():
      for doc_owner in self.__document_owners():
        doc_owner.add_viewed_documents(self.document)
      self.__update_seen_documents_on_read()
    elif self.is_mark_event():
      for doc_owner in self.__document_owners():
        doc_owner.add_marked_relevant_documents(self.document)
    elif self.is_serp_switch_event():
      last_rank_seen = (int(self.result_page) - 1) * serp_len()
      results_seen_by_now = self.query.results_up_to_rank(last_rank_seen) if last_rank_seen > 0 else []
      docs_seen_by_now = [result.document for result in results_seen_by_now]
      for doc_owner in self.__document_owners():
        doc_owner.add_seen_documents(*docs_seen_by_now)

  def __update_seen_documents_on_read(self):
    # FIXME: Query#_calculate_last_rank_reached uses the highest rank in any
    # action as the last rank reached. There's a mismatch here.

    # FIXME: THIS IS A HACK DUE TO RANK SOMETIMES BEING UNKNOWN, MARKED WITH -1
    if int(self.rank) > 0:
      try:
        seen_results = self.query.results_up_to_rank(self.rank)
        seen_docs = [result.document for result in seen_results]
        for doc_owner in self.__document_owners():
          doc_owner.add_seen_documents(*seen_docs)
      except RuntimeError as e:
        raise RuntimeError("Action at %s caused error: %s" % (self.timestamp, e))
    else:
      for doc_owner in self.__document_owners():
        doc_owner.add_seen_documents(self.document)

  def marked_relevant_documents(self):
    if self.is_mark_event():
      return [self.document]
    return []

  def viewed_documents(self):
    if self.action_type == Action.READ_ACTION_NAME:
      return [self.document]
    return []

  def seen_documents_since(self, rank):
    if self.action_type == Action.READ_ACTION_NAME:
      if int(self.rank) > 0:
        seen_results = self.query.results_between(rank, self.rank)
        return [result.document for result in seen_results]
      else:
        return [self.document]
    return []

  def __document_owners( self ):
    return [ self.session, self.query ]

  def __update_global_stats( self ):
    if hasattr( self, 'rank' ) and int(self.rank) > Action.global_highest_rank:
      Action.global_highest_rank = int(self.rank)

  def document_is_highly_relevant( self ):
    return self.document.is_highly_relevant_for_topic( self.session.topic )

  def document_is_moderately_relevant( self ):
    return self.document.is_moderately_relevant_for_topic( self.session.topic )

  def document_is_relevant( self ):
    return self.document.is_relevant_for_topic( self.session.topic )

  def gain(self, gain_levels):
    # Only doc-marked-relevant events can affect gain(
    if not self.is_mark_event():
      return 0
    if self.session.document_has_been_marked_relevant_before(self.document, self):
      return 0

    try:
      if self.document_is_moderately_relevant():
        return int(gain_levels[1])
      elif self.document_is_highly_relevant():
        return int(gain_levels[2])
      else:
        return int(gain_levels[0])
    except RuntimeError as e:
      raise RuntimeError("No gain could be inferred for doc-marked-relevant event at %s, query id %s: %s" %
                         (self.timestamp, self.query.record_id, e))

  def incidence_of_document(self):
    return self.session.incidence_of(self.document, self.query)

  def read_incidence_of_document(self, unique=False):
    previous_read_actions_of_current_document = self.session.actions_by_filter_before_action(
        lambda a: a.is_read_event() and a.document == self.document and (not unique or a.query != self.query),
        self
    )
    previous_incidences_count = len(previous_read_actions_of_current_document)
    if unique:
      previous_read_action_queries = set(map(lambda a: a[1].query, previous_read_actions_of_current_document))
      previous_incidences_count = len(previous_read_action_queries)
    return previous_incidences_count + (1 if unique or self.is_read_event() else 0)

  def unique_read_incidence_of_document(self):
    return self.read_incidence_of_document(unique=True)

  def is_read_event(self):
    return self.action_type == Action.READ_ACTION_NAME

  def mark_incidence_of_document(self, unique=False):
    previous_mark_actions_of_current_document = self.session.actions_by_filter_before_action(
        lambda a: a.is_mark_event() and a.document == self.document and (not unique or a.query != self.query),
        self
    )
    previous_incidences_count = len(previous_mark_actions_of_current_document)
    if unique:
      previous_mark_action_queries = set(map(lambda a: a[1].query, previous_mark_actions_of_current_document))
      previous_incidences_count = len(previous_mark_action_queries)
    return previous_incidences_count + (1 if unique or self.is_mark_event() else 0)

  def unique_mark_incidence_of_document(self):
    return self.mark_incidence_of_document(unique=True)

  def is_mark_event(self):
    return self.action_type == Action.MARK_ACTION_NAME

  def is_serp_switch_event(self):
    return self.action_type == Action.SERP_SWITCH_ACTION_NAME

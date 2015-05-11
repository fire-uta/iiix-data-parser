from datetime import datetime


from data_file import DataFile
from topic import Topic
from user import User
from query import Query
from condition import Condition
from action import Action
from session import Session


def _parse_line( line ):
  log_line_data_order = ['date', 'time', 'loglevel', 'user_id', 'condition',
    'topic_order_number', 'topic_id', 'action', 'action_parameters']
  line_as_list = line.strip().split(' ', len( log_line_data_order ) - 1)
  return dict(zip(log_line_data_order,line_as_list))


def _parse_datetime( date, time ):
  return datetime.strptime( date + ' ' + time, '%Y-%m-%d %H:%M:%S,%f' )


class LogFile(DataFile):

  def __init__(self, file_name):
    DataFile.__init__(self, file_name)
    result_file_info = self._get_file_info()
    self.topic = Topic.create_or_update( result_file_info['topic_id'] )
    self.user = User.create_or_update( result_file_info['user_id'] )
    self.query = Query.create_or_update( result_file_info['query_id'], topic = self.topic, user = self.user )
    self.condition = Condition.create_or_update( result_file_info['condition'] )
    self.__create_or_update_session()
    self.actions = self.__parse()
    self.topic.add_actions( self.actions )
    self.user.add_actions( self.actions )
    self.query.add_actions( self.actions )
    self.session.add_actions( self.actions )

  def __parse( self ):
    actions = []
    with open( self.file_name, 'rb' ) as log_file:
      for line in log_file:
          parsed_line = _parse_line( line )
          condition = self.condition
          timestamp = _parse_datetime( parsed_line['date'], parsed_line['time'] )
          action = Action( timestamp = timestamp, session = self.session,
            condition = condition, action_type = parsed_line['action'],
            query = self.query,
            action_parameters = parsed_line.get('action_parameters', None) )
          actions.append( action )

    return sorted(actions, key = lambda action: action.timestamp)

  def __create_or_update_session( self ):
    session_id = Session.build_session_id( self.user.record_id,
      self.topic.record_id )
    self.session = Session.create_or_update( session_id, user = self.user, topic = self.topic, condition = self.condition )

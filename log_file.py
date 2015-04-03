from datetime import datetime


from data_file import DataFile
from topic import Topic
from user import User
from query import Query
from condition import Condition
from action import Action


def _parse_line( line ):
  log_line_data_order = ['date', 'time', 'loglevel', 'user_id', 'condition',
    'topic_order_number', 'topic_id', 'action', 'action_parameters']
  line_as_list = line.split(' ', len( log_line_data_order ) - 1)
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
    self.actions = self.__parse()
    self.topic.add_actions( self.actions )
    self.user.add_actions( self.actions )
    self.query.add_actions( self.actions )

  def __parse( self ):
    actions = []
    with open( self.file_name, 'rb' ) as log_file:
      for line in log_file:
          parsed_line = _parse_line( line )
          user = User.create_or_update( parsed_line['user_id'] )
          condition = Condition.create_or_update( parsed_line['condition'] )
          topic = Topic.create_or_update( parsed_line['topic_id'] )
          timestamp = _parse_datetime( parsed_line['date'], parsed_line['time'] )
          action = Action( timestamp = timestamp, user = user, condition = condition,
            topic = topic, action_type = parsed_line['action'],
            action_parameters = parsed_line.get('action_parameters', None) )
          actions.append( action )

    return actions

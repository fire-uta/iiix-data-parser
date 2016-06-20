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


class CombinedLogFile(DataFile):

  def __init__(self, file_name):
    DataFile.__init__(self, file_name)
    self.query_counter = 0
    self.actions = self.__parse()

  def __parse( self ):
    actions = []
    query_text = None
    with open( self.file_name, 'r' ) as log_file:
      for line in log_file:
          parsed_line = _parse_line( line )

          if parsed_line['action'] == 'QUERY_ISSUED' or parsed_line['action'] == 'QUERY_SUGGESTION_ISSUED':
            self.query_counter += 1
            query_text = parsed_line.get('action_parameters', None)
            #print ("%s - %s - X - %s: %s" % (self.query_counter, parsed_line['user_id'], parsed_line['topic_id'], query_text))

          topic = Topic.create_or_update( parsed_line['topic_id'] )
          user = User.create_or_update( parsed_line['user_id'] )
          condition = Condition.create_or_update( parsed_line['condition'] )

          session = self.__create_or_update_session( user, topic, condition )

          query_id = str( self.query_counter )
          query = Query.create_or_update( query_id, topic = topic, user = user, session = session, query_text = query_text )

          timestamp = _parse_datetime( parsed_line['date'], parsed_line['time'] )
          action = Action( timestamp = timestamp, session = session,
            condition = condition, action_type = parsed_line['action'],
            query = query,
            action_parameters = parsed_line.get('action_parameters', None) )
          actions.append( action )

          topic.add_actions( [action] )
          user.add_actions( [action] )
          query.add_actions( [action] )
          session.add_actions( [action] )
          session.add_query( query )

    return sorted(actions, key = lambda action: action.timestamp)

  def __create_or_update_session( self, user, topic, condition ):
    session_id = Session.build_session_id( user.record_id,
      topic.record_id )
    return Session.create_or_update( session_id, user = user, topic = topic, condition = condition )

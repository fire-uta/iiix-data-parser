import csv


from topic import Topic
from query import Query
from document import Document
from data_file import DataFile
from user import User
from condition import Condition


class QueriesSummaryFile(DataFile):
  def __init__(self, file_name):
    DataFile.__init__(self, file_name)
    self.__parse()

  def __parse( self ):
    with open( self.file_name, 'rb' ) as result_file:
      result_reader = csv.DictReader( result_file, delimiter=',')
      for row in result_reader:
          topic = Topic.create_or_update( row['topic'] )
          user = User.create_or_update( row['userid'] )
          condition = Condition.create_or_update( row['condition'] )
          autocomplete = row['autocomplete_used'] == 1
          query = Query.create_or_update( row['queryid'], topic = topic, user = user, condition = condition, autocomplete = autocomplete, query_text = row['terms'] )

import csv
import re


from topic import Topic
from query import Query
from document import Document
from data_file import DataFile
from user import User


class ResultFile(DataFile):
  def __init__(self, file_name):
    DataFile.__init__(self, file_name)
    result_file_info = self._get_file_info()
    self.topic = Topic.create_or_update( result_file_info['topic_id'] )
    self.user = User.create_or_update( result_file_info['user_id'] )
    self.query = Query.create_or_update( result_file_info['query_id'], topic = self.topic, user = self.user )
    self.__parse()

  def __parse( self ):
    try:
      with open( self.file_name, 'r' ) as result_file:
        result_reader = csv.DictReader( result_file, delimiter=',')
        for row in result_reader:
            document = Document.create_or_update( row['docid'].strip() )
            self.query.add_to_result_list( row['rank'].strip(), document )
            self.topic.add_relevance( document, row['trec_judgement'].strip() )
    except ValueError as e:
      raise RuntimeError( "File %s contains invalid data: %s" % ( self.file_name, e ) )

import csv
import re
import ntpath


from topic import Topic
from query import Query
from document import Document


class DataFile:
  def __init__(self, file_name):
    self.file_name = file_name
    self.bare_file_name = self.__get_bare_file_name()

  def __get_bare_file_name( self ):
    head, tail = ntpath.split( self.file_name )
    return tail or ntpath.basename( head )

  def _get_file_info( self ):
    match = re.match( '([^-]+)-([^-]+)-([^-]+)-([^.]+)\.+?', self.bare_file_name )
    if match is None: raise RuntimeError( "Unknown %s encountered: %s" % (self.__class__, self.file_name) )
    return {
        'query_id': match.group(1),
        'user_id': match.group(2),
        'condition': match.group(3),
        'topic_id': match.group(4)
    }

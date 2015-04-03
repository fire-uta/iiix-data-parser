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

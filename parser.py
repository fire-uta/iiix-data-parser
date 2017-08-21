import sys
import os
import csv


import numpy


import data_export
import statistics


from result_file import ResultFile
from queries_summary_file import QueriesSummaryFile
from log_file import LogFile
from combined_log_file import CombinedLogFile
from document import Document
from query import Query
from topic import Topic
from user import User
from condition import Condition
from action import Action
from session import Session
from relevance import Relevance
from filterable import Filterable
from session_time_slice import SessionTimeSlice
from cli import CLI


def error_exit():
  sys.stderr.write('ERROR: missing argument(s).\n')
  CLI.parser.print_help()
  sys.exit(1)


def get_cli_options():
  (options, args) = CLI.parsedArgs
  return options


def parse_result_files(cli_options):
  result_files = []
  results_dir = cli_options.results
  if results_dir is None: error_exit()
  for dirname, dirnames, filenames in os.walk( results_dir ):
    files_count = len( filenames )
    every_tenth = int( files_count / 10 )
    sys.stdout.write( "Parsing %i result files" % files_count )
    for idx, filename in enumerate(filenames):
      if not filename.endswith('.serp'): continue
      sys.stdout.write( '.' )
      if idx % every_tenth == 0: sys.stdout.write(str(idx))
      sys.stdout.flush()
      result_files.append( ResultFile( os.path.join( dirname, filename ) ) )
  sys.stdout.write( '\n' )
  return result_files


def parse_log_files(cli_options):
  log_files = []
  log_dir = cli_options.logs
  if log_dir is None: error_exit()
  for dirname, dirnames, filenames in os.walk( log_dir ):
    files_count = len( filenames )
    every_tenth = int( files_count / 10 ) or 1
    sys.stdout.write( "Parsing %i log files" % files_count )
    for idx, filename in enumerate(filenames):
      if not filename.endswith('.log'): continue
      sys.stdout.write( '.' )
      if idx % every_tenth == 0: sys.stdout.write(str(idx))
      sys.stdout.flush()
      if cli_options.use_combined_log_parser:
        log_files.append( CombinedLogFile( os.path.join( dirname, filename ) ) )
      else:
        log_files.append( LogFile( os.path.join( dirname, filename ) ) )
  sys.stdout.write( '\n' )
  return log_files


def parse_gains(cli_options):
  gains = cli_options.gains
  if gains is None:
    error_exit()
  return [int(i) for i in gains.split(",")]


def get_queries_file_name(cli_options):
  if cli_options.queries is None:
    error_exit()
  return cli_options.queries


def parse():
  cli_options = get_cli_options()
  gains = parse_gains(cli_options)
  result_files = parse_result_files(cli_options)
  log_files = parse_log_files(cli_options)
  queries_file = QueriesSummaryFile(get_queries_file_name(cli_options))
  return {
      'cli_options': cli_options,
      'gains': gains,
      'result_files': result_files,
      'log_files': log_files,
      'queries_file': queries_file
  }

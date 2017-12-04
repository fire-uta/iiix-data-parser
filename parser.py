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


def estimate_single_serp_query_scan_actions(query, npass=1):
  scan_count_before = len(query.seen_documents)
  scan_time_used = query.total_snippet_scanning_time_in_seconds()
  number_of_documents_likely_seen = int(scan_time_used / query.session.average_snippet_scanning_time_in_seconds())
  results_likely_seen = query.results_up_to_rank(number_of_documents_likely_seen) if number_of_documents_likely_seen > 0 else []
  docs_likely_seen = [result.document for result in results_likely_seen]
  for doc_owner in [query, query.session]:
    doc_owner.add_seen_documents(*docs_likely_seen)

  # Make multiple passes until scanned documents count stabilizes
  if len(query.seen_documents) != scan_count_before:
    if npass == 1:
      sys.stdout.write('F')
    sys.stdout.write(str(npass))
    estimate_single_serp_query_scan_actions(query, npass + 1)


def estimate_last_serp_query_scan_actions(query, npass=1):
  scan_count_before = len(query.seen_documents)
  last_serp_actions = query.last_serp_actions(plain_actions=False)
  # FIXME: assumes 0 duration for last actions in query
  time_used = sum(map(lambda d: 0 if d is None else d, [query.action_duration_in_seconds_for(idx, a) for idx, a in last_serp_actions]))
  number_of_documents_likely_seen = int(time_used / query.session.average_snippet_scanning_time_in_seconds())
  last_serp_first_rank = (query.last_serp_number() - 1) * serp_len() + 1
  results_likely_seen = query.results_between(last_serp_first_rank, last_serp_first_rank + number_of_documents_likely_seen - 1) if number_of_documents_likely_seen > 0 else []
  docs_likely_seen = [result.document for result in results_likely_seen]
  for doc_owner in [query, query.session]:
    doc_owner.add_seen_documents(*docs_likely_seen)

  # Make multiple passes until scanned documents count stabilizes
  if len(query.seen_documents) != scan_count_before:
    if npass == 1:
      sys.stdout.write('L')
    sys.stdout.write(str(npass))
    estimate_last_serp_query_scan_actions(query, npass + 1)


def refine_scan_action_estimates():
  # FIXME: Should also check last SERPs of all queries (no clicks after page switch -> no record of scans)
  queries_count = Query.count()
  every_tenth = int(queries_count / 10)
  sys.stdout.write("Refining scan action estimates for %i queries..." % queries_count)
  current_queries_count = 0
  for session in Session.all():
    for query in session.sorted_queries():
      current_queries_count += 1
      sys.stdout.write('.')
      if current_queries_count % every_tenth == 0:
        sys.stdout.write('-' + str(current_queries_count) + '-')
      sys.stdout.flush()
      # First page examined but nothing clicked -> no record of scanned snippets
      # Estimate scans by looking at total scanning time, and comparing to average scanning time
      if len(query.document_read_actions()) == 0 and query.never_switched_from_first_serp():
        estimate_single_serp_query_scan_actions(query)
      elif query.no_document_actions_on_last_serp():
        estimate_last_serp_query_scan_actions(query)
  sys.stdout.write('\n')


def parse():
  cli_options = get_cli_options()
  gains = parse_gains(cli_options)
  result_files = parse_result_files(cli_options)
  log_files = parse_log_files(cli_options)
  queries_file = QueriesSummaryFile(get_queries_file_name(cli_options))
  refine_scan_action_estimates()
  return {
      'cli_options': cli_options,
      'gains': gains,
      'result_files': result_files,
      'log_files': log_files,
      'queries_file': queries_file
  }


def serp_len():
  serp_len = get_cli_options().serp_len
  if serp_len is None:
    error_exit()
  return int(serp_len)

import sys
import optparse
import os


from result_file import ResultFile
from queries_summary_file import QueriesSummaryFile
from log_file import LogFile
from document import Document
from query import Query
from topic import Topic
from user import User
from condition import Condition
from action import Action


def error_exit():
  sys.stderr.write( 'ERROR: missing argument(s).\n' )
  CLI.parser.print_help()
  sys.exit(1)


class CLI: pass
CLI.parser = optparse.OptionParser()
CLI.parser.add_option( "-q", "--queries", dest = "queries", help = "Queries csv file", metavar="FILE")
CLI.parser.add_option( "-l", "--logs", dest = "logs", help = "Path to log files containing directory", metavar="DIR")
CLI.parser.add_option( "-r", "--results", dest = "results", help = "Path to result files containing directory", metavar="DIR")
CLI.parsedArgs = CLI.parser.parse_args()


def get_cli_options():
  (options, args) = CLI.parsedArgs
  return options


def parse_result_files():
  result_files = []
  opts = get_cli_options()
  results_dir = opts.results
  if results_dir is None: error_exit()
  sys.stdout.write( 'Parsing result files' )
  for dirname, dirnames, filenames in os.walk( results_dir ):
    for filename in filenames:
      if not filename.endswith('.serp'): continue
      sys.stdout.write( '.' )
      sys.stdout.flush()
      result_files.append( ResultFile( os.path.join( dirname, filename ) ) )
  sys.stdout.write( '\n' )
  return result_files


def parse_log_files():
  log_files = []
  opts = get_cli_options()
  log_dir = opts.logs
  if log_dir is None: error_exit()
  sys.stdout.write( 'Parsing log files' )
  for dirname, dirnames, filenames in os.walk( log_dir ):
    for filename in filenames:
      if not filename.endswith('.log'): continue
      sys.stdout.write( '.' )
      sys.stdout.flush()
      log_files.append( LogFile( os.path.join( dirname, filename ) ) )
  sys.stdout.write( '\n' )
  return log_files


def get_queries_file_name():
  opts = get_cli_options()
  if opts.queries is None: error_exit()
  return opts.queries


result_files = parse_result_files()
log_files = parse_log_files()
queries_file = QueriesSummaryFile( get_queries_file_name() )

print "Queries: %i" % len(Query.store)
print "Topics: %i: %s" % (len(Topic.store), Topic.store.keys())
print "Users: %i" % len(User.store)
print "Documents: %i" % len(Document.store)
print "Conditions: %i: %s" % (len(Condition.store), Condition.store.keys())
print "Action types: %i: %s" % (len(Action.type_dict.keys()), Action.type_dict.keys())

print "Mark-doc-as-viewed actions: %i" % (
  len(Action.by_type('DOC_MARKED_VIEWED')))
print "Mark-doc-as-viewed actions with a moderately relevant doc: %i" % (
  len(Action.filter_by_type('DOC_MARKED_VIEWED', Action.moderately_relevant_filter)))
print "Mark-doc-as-viewed actions with a highly relevant doc: %i" % (
  len(Action.filter_by_type('DOC_MARKED_VIEWED', Action.highly_relevant_filter)))

print "Mark-doc-as-relevant actions: %i" % (
  len(Action.by_type('DOC_MARKED_RELEVANT')))
print "Mark-doc-as-relevant actions with a moderately relevant doc: %i" % (
  len(Action.filter_by_type('DOC_MARKED_RELEVANT', Action.moderately_relevant_filter)))
print "Mark-doc-as-relevant actions with a highly relevant doc: %i" % (
  len(Action.filter_by_type('DOC_MARKED_RELEVANT', Action.highly_relevant_filter)))

print "Mark-doc-as-viewed actions with no delays: %i" % (
  len(Action.filter_by_type('DOC_MARKED_VIEWED', Action.no_delays_filter)))
print "Mark-doc-as-viewed actions with no delays and moderately relevant doc: %i" % (
  len(Action.filter_by_type('DOC_MARKED_VIEWED', Action.combine_filters( Action.no_delays_filter, Action.moderately_relevant_filter))))
print "Mark-doc-as-viewed actions with no delays and highly relevant doc: %i" % (
  len(Action.filter_by_type('DOC_MARKED_VIEWED', Action.combine_filters( Action.no_delays_filter, Action.highly_relevant_filter))))

print "Mark-doc-as-relevant actions with no delays: %i" % (
  len(Action.filter_by_type('DOC_MARKED_RELEVANT', Action.no_delays_filter)))
print "Mark-doc-as-relevant actions with no delays and moderately relevant doc: %i" % (
  len(Action.filter_by_type('DOC_MARKED_RELEVANT', Action.combine_filters( Action.no_delays_filter, Action.moderately_relevant_filter))))
print "Mark-doc-as-relevant actions with no delays and highly relevant doc: %i" % (
  len(Action.filter_by_type('DOC_MARKED_RELEVANT', Action.combine_filters( Action.no_delays_filter, Action.highly_relevant_filter))))

print "Mark-doc-as-viewed actions with query delays: %i" % (
  len(Action.filter_by_type('DOC_MARKED_VIEWED', Action.query_delay_filter)))
print "Mark-doc-as-viewed actions with query delays and moderately relevant doc: %i" % (
  len(Action.filter_by_type('DOC_MARKED_VIEWED', Action.combine_filters( Action.query_delay_filter, Action.moderately_relevant_filter))))
print "Mark-doc-as-viewed actions with query delays and highly relevant doc: %i" % (
  len(Action.filter_by_type('DOC_MARKED_VIEWED', Action.combine_filters( Action.query_delay_filter, Action.highly_relevant_filter))))

print "Mark-doc-as-relevant actions with query delays: %i" % (
  len(Action.filter_by_type('DOC_MARKED_RELEVANT', Action.query_delay_filter)))
print "Mark-doc-as-relevant actions with query delays and moderately relevant doc: %i" % (
  len(Action.filter_by_type('DOC_MARKED_RELEVANT', Action.combine_filters( Action.query_delay_filter, Action.moderately_relevant_filter))))
print "Mark-doc-as-relevant actions with query delays and highly relevant doc: %i" % (
  len(Action.filter_by_type('DOC_MARKED_RELEVANT', Action.combine_filters( Action.query_delay_filter, Action.highly_relevant_filter))))

print "Mark-doc-as-viewed actions with document delays: %i" % (
  len(Action.filter_by_type('DOC_MARKED_VIEWED', Action.document_delay_filter)))
print "Mark-doc-as-viewed actions with document delays and moderately relevant doc: %i" % (
  len(Action.filter_by_type('DOC_MARKED_VIEWED', Action.combine_filters( Action.document_delay_filter, Action.moderately_relevant_filter))))
print "Mark-doc-as-viewed actions with document delays and highly relevant doc: %i" % (
  len(Action.filter_by_type('DOC_MARKED_VIEWED', Action.combine_filters( Action.document_delay_filter, Action.highly_relevant_filter))))

print "Mark-doc-as-relevant actions with document delays: %i" % (
  len(Action.filter_by_type('DOC_MARKED_RELEVANT', Action.document_delay_filter)))
print "Mark-doc-as-relevant actions with document delays and moderately relevant doc: %i" % (
  len(Action.filter_by_type('DOC_MARKED_RELEVANT', Action.combine_filters( Action.document_delay_filter, Action.moderately_relevant_filter))))
print "Mark-doc-as-relevant actions with document delays and highly relevant doc: %i" % (
  len(Action.filter_by_type('DOC_MARKED_RELEVANT', Action.combine_filters( Action.document_delay_filter, Action.highly_relevant_filter))))

print "Mark-doc-as-viewed actions with both delays: %i" % (
  len(Action.filter_by_type('DOC_MARKED_VIEWED', Action.combined_delay_filter)))
print "Mark-doc-as-viewed actions with both delays and moderately relevant doc: %i" % (
  len(Action.filter_by_type('DOC_MARKED_VIEWED', Action.combine_filters( Action.combined_delay_filter, Action.moderately_relevant_filter))))
print "Mark-doc-as-viewed actions with both delays and highly relevant doc: %i" % (
  len(Action.filter_by_type('DOC_MARKED_VIEWED', Action.combine_filters( Action.combined_delay_filter, Action.highly_relevant_filter))))

print "Mark-doc-as-relevant actions with both delays: %i" % (
  len(Action.filter_by_type('DOC_MARKED_RELEVANT', Action.combined_delay_filter)))
print "Mark-doc-as-relevant actions with both delays and moderately relevant doc: %i" % (
  len(Action.filter_by_type('DOC_MARKED_RELEVANT', Action.combine_filters( Action.combined_delay_filter, Action.moderately_relevant_filter))))
print "Mark-doc-as-relevant actions with both delays and highly relevant doc: %i" % (
  len(Action.filter_by_type('DOC_MARKED_RELEVANT', Action.combine_filters( Action.combined_delay_filter, Action.highly_relevant_filter))))

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
  for dirname, dirnames, filenames in os.walk( results_dir ):
    for filename in filenames:
      if not filename.endswith('.serp'): continue
      result_files.append( ResultFile( os.path.join( dirname, filename ) ) )
  return result_files


def parse_log_files():
  log_files = []
  opts = get_cli_options()
  log_dir = opts.logs
  if log_dir is None: error_exit()
  for dirname, dirnames, filenames in os.walk( log_dir ):
    for filename in filenames:
      if not filename.endswith('.log'): continue
      log_files.append( LogFile( os.path.join( dirname, filename ) ) )
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

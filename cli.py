import optparse


class CLI: pass
CLI.parser = optparse.OptionParser()
CLI.parser.add_option( "-q", "--queries", dest = "queries", help = "Queries csv file", metavar="FILE")
CLI.parser.add_option( "-l", "--logs", dest = "logs", help = "Path to log files containing directory", metavar="DIR")
CLI.parser.add_option( "-r", "--results", dest = "results", help = "Path to result files containing directory", metavar="DIR")
CLI.parser.add_option( "-g", "--gains", dest = "gains", help = "Comma-separated list of gains for different relevance levels, eg. 0,1,10", metavar="LIST")
CLI.parser.add_option( "-c", action="store_true", dest="use_combined_log_parser", help = "Use combined log parser" )
CLI.parser.add_option( "-a", action="store_true", dest="use_alt_log_format", help = "Use alternative log format" )
CLI.parsedArgs = CLI.parser.parse_args()

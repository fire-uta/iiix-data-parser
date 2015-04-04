from numpy import uint16


class QueryResultDocument:
  def __init__(self, result_list, rank, document):
    self.result_list = result_list
    self.rank = uint16(rank)
    self.document = document

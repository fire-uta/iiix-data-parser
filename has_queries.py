class HasQueries:
  def __init__(self):
    self.queries = {}

  def add_queries(self, *queries):
    for query in queries:
      self.add_query(query)

  def add_query(self, query):
    self.queries[query.record_id] = query

  def query_formulation_times(self):
    return [query.formulation_time_in_seconds() for query in self.queries.values()]

  def first_query(self):
    found_query = None
    for query in self.queries.values():
      if found_query is None or query.get_start_timestamp() < found_query.get_start_timestamp():
        found_query = query
    return found_query

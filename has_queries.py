from attr_utils import _memoize_attr


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

  def queries_prior_to(self, test_query):
    return _memoize_attr(
        self,
        '_queries_prior_to_' + str(test_query.record_id),
        lambda: self._calculate_queries_prior_to(test_query)
    )

  def _calculate_queries_prior_to(self, test_query):
    found_queries = []
    for query in self.queries.values():
      if query.get_start_timestamp() < test_query.get_start_timestamp():
        found_queries.append(query)
    return found_queries

  def query_formulation_events(self):
    formulation_events = []
    for query in self.queries.values():
      formulation_events.append(query.formulation_event())
    return formulation_events

  def sorted_queries(self):
    return _memoize_attr(
        self,
        '_sorted_queries',
        lambda: sorted(self.queries.values(), key=lambda q: q.get_start_timestamp())
    )

  def incidence_of(self, document, query):
    prior_queries = self.queries_prior_to(query)
    return sum([1 if prior_query.has_been_seen(document) else 0 for prior_query in prior_queries]) + 1

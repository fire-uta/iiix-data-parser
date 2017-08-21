from datetime import timedelta

from acts_as_session import ActsAsSession


class SessionTimeSlice(ActsAsSession):
  def __init__(self, session, start_msecs, length_msecs, preceding_slice=None):
    ActsAsSession.__init__(self, session.user, session.topic, session.condition)
    self.session = session
    self.start_msecs = start_msecs
    self.length_msecs = length_msecs
    self.session_start_at = self.session.get_start_timestamp()
    self.slice_start_at = self.session_start_at + timedelta(milliseconds=self.start_msecs)
    self.slice_stop_at = self.slice_start_at + timedelta(milliseconds=self.length_msecs)
    self.preceding_slice = preceding_slice

    self._resolve_actions()
    self._resolve_queries()
    self._resolve_documents()

  def has_been_viewed_in_preceding_slices(self, document):
    if self.preceding_slice is None:
      return False
    if self.preceding_slice.has_been_viewed(document):
      return True
    return self.preceding_slice.has_been_viewed_in_preceding_slices(document)

  def has_been_seen_in_preceding_slices(self, document):
    if self.preceding_slice is None:
      return False
    if self.preceding_slice.has_been_seen(document):
      return True
    return self.preceding_slice.has_been_seen_in_preceding_slices(document)

  def has_been_marked_in_preceding_slices(self, document):
    if self.preceding_slice is None:
      return False
    if self.preceding_slice.has_been_marked(document):
      return True
    return self.preceding_slice.has_been_marked_in_preceding_slices(document)

  def add_viewed_documents(self, *documents):
    for document in documents:
      if not self.has_been_viewed_in_preceding_slices(document):
        super().add_viewed_documents(document)

  def add_seen_documents(self, *documents):
    for document in documents:
      if not self.has_been_seen_in_preceding_slices(document):
        super().add_seen_documents(document)

  def add_marked_documents(self, *documents):
    for document in documents:
      if not self.has_been_marked_in_preceding_slices(document):
        super().add_marked_documents(document)

  def _resolve_actions(self):
    self.add_actions(list(filter(self._action_resolver(), self.session.actions)))

  def _resolve_queries(self):
    self.add_queries(*list(filter(self._query_resolver(), self.session.queries.values())))

  def _resolve_documents(self):
    first_query = self.first_query()
    for action in self.actions:
      self.add_viewed_documents(*(action.viewed_documents()))
      self.add_marked_relevant_documents(*(action.marked_relevant_documents()))
      if action.query.record_id == first_query.record_id:
        self.add_seen_documents(*action.seen_documents_since(self._first_rank()))
      else:
        self.add_seen_documents(*action.seen_documents_since(1))

  def _action_resolver(self):
    return lambda action: action.timestamp < self.slice_stop_at and action.timestamp > self.slice_start_at

  def _query_resolver(self):
    return lambda query: query.get_start_timestamp() <= self.slice_stop_at and self.slice_start_at <= query.get_end_timestamp()

  def _first_rank(self):
    first_query = self.first_query()
    found_rank = None
    for action in self.actions:
      # Note: We have to check for rank > 0 since sometimes the log contains odd stuff there
      if action.query.record_id != first_query.record_id:
        break
      if hasattr(action, 'rank') and int(action.rank) > 0 and (found_rank is None or int(action.rank) < int(found_rank)):
        found_rank = action.rank

    # This is the case where time slice begins right at the end of a query, or between them
    # if found_rank is None:
    #   found_rank = 1

    return found_rank

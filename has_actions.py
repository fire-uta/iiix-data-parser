from attr_utils import _memoize_attr


from action import Action


class HasActions:
  def add_actions(self, actions):
    if not hasattr(self, 'actions'):
      self.actions = []
    self.actions.extend(actions)
    self.actions = sorted(self.actions, key=lambda action: action.timestamp)

  def actions_by_type(self, action_type):
    return self.actions_by_filter(lambda a: a.action_type == action_type)

  def actions_by_type_until(self, action_type, seconds):
    return _memoize_attr(
        self,
        '_actions_by_' + str(action_type) + '_type_until_' + str(seconds),
        lambda: self._calculate_actions_by_type_until(action_type, seconds)
    )

  def actions_by_filter(self, filter_func=lambda a: False):
    return [(idx, action) for idx, action in enumerate(self.actions) if filter_func(action)]

  def _calculate_actions_by_type_until(self, action_type, seconds):
    return self._calculate_actions_by_filter_until(lambda a: a.action_type == action_type, seconds)

  def _calculate_actions_by_filter_until(self, filter_func=lambda a: False, seconds=0):
    actions = []
    for idx, action in enumerate(self.actions):
      if self.seconds_elapsed_at(action.timestamp) > seconds:
        break
      if filter_func(action):
        actions.append((idx, action))
    return actions

  def actions_by_filter_before_action(self, filter_func, target_action):
    actions = []
    for idx, action in enumerate(self.actions):
      if action == target_action:
        break
      if filter_func(action):
        actions.append((idx, action))
    return actions

  def action_duration_in_seconds_for(self, idx, action, end_action_type=None):
    next_timestamp = None
    if end_action_type is None:
      try:
        next_timestamp = self.actions[idx + 1].timestamp
      except IndexError:
        # Can not calculate duration if the action is dead last
        return None
    else:
      for ii in range(idx + 1, len(self.actions) - 1, 1):
        next_action = self.actions[ii]
        if next_action.action_type == end_action_type:
          next_timestamp = next_action.timestamp
          break
    # Duration can not be calculated if a next action was not found
    if next_timestamp is None:
      return None
    current_timestamp = action.timestamp
    delta = next_timestamp - current_timestamp
    return delta.total_seconds()

  def duration_in_seconds(self):
    # No actions? No duration.
    if len(self.actions) == 0:
      return None
    first_timestamp = self.get_start_timestamp()
    last_timestamp = self.get_end_timestamp()
    delta = last_timestamp - first_timestamp
    return delta.total_seconds()

  def get_start_timestamp(self):
    # No actions?
    if len(self.actions) == 0:
      return None
    return _memoize_attr(
        self,
        '_start_timestamp',
        lambda: self.actions[0].timestamp
    )

  def get_end_timestamp(self):
    # No actions?
    if len(self.actions) == 0:
      return None
    return self.actions[-1].timestamp

  def document_read_actions(self):
    return self.actions_by_type(Action.READ_ACTION_NAME)

  def document_read_actions_until(self, seconds):
    return self.actions_by_type_until(Action.READ_ACTION_NAME, seconds)

  def document_marked_relevant_actions(self):
    return self.actions_by_type(Action.MARK_ACTION_NAME)

  def document_marked_relevant_actions_until(self, seconds):
    return self.actions_by_type_until(Action.MARK_ACTION_NAME, seconds)

  def document_read_times(self):
    read_times = {}
    for read_event in self.document_read_events():
      document_id = read_event['document'].record_id
      duration = read_event['read_duration']
      if document_id in read_times:
        read_times[document_id] += duration
      else:
        read_times[document_id] = duration
    return read_times

  def document_read_events(self):
    read_events = []
    for idx, action in self.document_read_actions():
      action_duration = self.action_duration_in_seconds_for(idx, action)
      if action_duration is None:
        # It's possible that the duration can not be calculated (for session time slices)
        continue
      document = action.document
      rank = action.query.rank_of(document)
      result = action.query.result_at(rank) if rank is not None else None
      read_events.append({
          'document': document,
          'result': result,
          'read_duration': action_duration,
          'read_start_at_seconds': self.seconds_elapsed_at(action.timestamp),
          'rank': rank,
          'query': action.query,
          'continuous_rank': action.query.continuous_rank_at(rank) if rank is not None else None,
          'query_order_number': action.query.order_number(),
          'document_incidence': action.incidence_of_document(),
          'read_incidence': action.read_incidence_of_document(),
          'read_incidence_unique': action.unique_read_incidence_of_document()
      })
    return read_events

  def document_marked_relevant_events(self):
    mark_events = []
    for idx, action in self.document_marked_relevant_actions():
      action_duration = self.action_duration_in_seconds_for(idx, action)
      if action_duration is None:
        # It's possible that the duration can not be calculated (for session time slices)
        continue
      document = action.document
      rank = action.query.rank_of(document)
      mark_events.append({
          'document': document,
          'mark_duration': action_duration,
          'mark_start_at_seconds': self.seconds_elapsed_at(action.timestamp),
          'rank': rank,
          'continuous_rank': action.query.continuous_rank_at(rank) if rank is not None else None,
          'query_order_number': action.query.order_number(),
          'document_incidence': action.incidence_of_document(),
          'read_incidence': action.read_incidence_of_document(),
          'mark_incidence': action.mark_incidence_of_document(),
          'read_incidence_unique': action.unique_read_incidence_of_document(),
          'mark_incidence_unique': action.unique_mark_incidence_of_document()
      })
    return mark_events

  def snippet_scan_events(self):
    scan_events = []
    for idx, action in self.snippet_scan_actions():
      action_duration = self.action_duration_in_seconds_for(idx, action)
      if action_duration is None:
        # It's possible that the duration can not be calculated (for session time slices)
        continue
      document = action.document
      read_events.append({
          'document': document,
          'read_duration': action_duration,
          'read_start_at_seconds': self.seconds_elapsed_at(action.timestamp)
      })
    return read_events

  def seconds_elapsed_at(self, timestamp):
    return _memoize_attr(
        self,
        '_seconds_elapsed_at_' + str(timestamp),
        lambda: (timestamp - self.get_start_timestamp()).total_seconds()
    )

  def average_snippet_scanning_time_in_seconds(self):
    if len(self.seen_documents) == 0:
      return None
    return self.total_snippet_scanning_time_in_seconds() / len(self.seen_documents)

  def document_read_start_at_seconds(self, document):
    for idx, action in self.document_read_actions():
      if hasattr(action, 'document_id') and action.document_id == document.record_id:
        return self.seconds_elapsed_at(action.timestamp)
    return None

  def document_mark_start_at_seconds(self, document):
    for idx, action in self.document_marked_relevant_actions():
      if hasattr(action, 'document_id') and action.document_id == document.record_id:
        return self.seconds_elapsed_at(action.timestamp)
    return None

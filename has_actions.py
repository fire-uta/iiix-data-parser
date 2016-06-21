class HasActions:
  def add_actions(self, actions):
    if not hasattr(self, 'actions'):
      self.actions = []
    self.actions.extend(actions)
    self.actions = sorted(self.actions, key=lambda action: action.timestamp)

  def actions_by_type(self, action_type):
    return [(idx, action) for idx, action in enumerate(self.actions) if action.action_type == action_type]

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
    return self.actions[0].timestamp

  def get_end_timestamp(self):
    # No actions?
    if len(self.actions) == 0:
      return None
    return self.actions[-1].timestamp

  def document_read_actions(self):
    return self.actions_by_type('DOC_MARKED_VIEWED')

  def document_marked_relevant_actions(self):
    return self.actions_by_type('DOC_MARKED_RELEVANT')

  def document_read_times(self):
    read_actions = self.document_read_actions()
    read_times = {}
    for idx, action in read_actions:
      action_duration = self.action_duration_in_seconds_for(idx, action)
      if action_duration is None:
        # It's possible that the duration can not be calculated (for session time slices)
        continue
      document = action.document
      if document.record_id in read_times:
        read_times[document.record_id] += action_duration
      else:
        read_times[document.record_id] = action_duration
    return read_times

  def seconds_elapsed_at(self, timestamp):
    return (timestamp - self.get_start_timestamp()).total_seconds()

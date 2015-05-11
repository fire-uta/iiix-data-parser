class HasActions:
  def add_actions(self, actions):
    if not hasattr( self, 'actions' ):
      self.actions = []
    self.actions.extend( actions )
    self.actions = sorted( self.actions, key = lambda action: action.timestamp )

  def actions_by_type( self, action_type ):
    return [(idx,action) for idx, action in enumerate(self.actions) if action.action_type == action_type]

  def action_duration_in_seconds_for( self, idx, action, end_action_type = None ):
    next_timestamp = None
    if end_action_type is None:
      next_timestamp = self.actions[ idx + 1 ].timestamp
    else:
      for ii in range( idx + 1, len(self.actions) - 1, 1 ):
        next_action = self.actions[ii]
        if next_action.action_type == end_action_type:
          next_timestamp = next_action.timestamp
          break
    current_timestamp = action.timestamp
    delta = next_timestamp - current_timestamp
    return delta.total_seconds()

class HasActions:
  def add_actions(self, actions):
    if not hasattr( self, 'actions' ):
      self.actions = []
    self.actions.extend( actions )

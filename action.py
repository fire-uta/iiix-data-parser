class Action:
  def __init__(self, timestamp, user, condition, topic, action_type, action_parameters):
    self.timestamp = timestamp
    self.user = user
    self.condition = condition
    self.topic = topic
    self.action_type = action_type
    self.action_parameters = action_parameters

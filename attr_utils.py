def _set_attr(obj, attr_name, value_func):
  setattr(obj, attr_name, value_func())
  return getattr(obj, attr_name)


def _memoize_attr(obj, attr_name, value_func):
  try:
    return getattr(obj, attr_name)
  except AttributeError:
    return _set_attr(obj, attr_name, value_func)

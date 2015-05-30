def _set_attr( obj, attr_name, value_to_set ):
  setattr( obj, attr_name, value_to_set )
  return getattr( obj, attr_name )

def _memoize_attr( obj, attr_name, value_to_set ):
  return getattr( obj, attr_name, _set_attr( obj, attr_name, value_to_set ) )

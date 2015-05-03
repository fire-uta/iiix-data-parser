class DataRecord:

  @classmethod
  def get_store( cls ):
    if hasattr( cls, 'store' ): return cls.store
    cls.store = {}
    return cls.store

  @classmethod
  def find( cls, record_id ):
    return cls.get_store().get( str(record_id), None )

  @classmethod
  def save( cls, record_id, record ):
    cls.get_store()[ str(record_id) ] = record

  @classmethod
  def create_or_update( cls, record_id, **kwargs ):
    found_record = cls.find( str(record_id) )
    if found_record is not None:
      for name, value in kwargs.items():
        setattr( found_record, name, value )
      return found_record
    return cls( str(record_id), **kwargs )

  def __init__( self, record_id ):
    self.record_id = str(record_id)
    self.__class__.save( str(record_id), self )


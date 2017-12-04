import csv

from numpy import uint8


def field_name_for_csv_export_value(key, value):
  if key == 'record_id':
    return 'id'
  if isinstance(value, DataRecord):
    return key + '_id'
  return key


def csv_export_value(value):
  if isinstance(value, DataRecord):
    return value.record_id
  else:
    return value


class DataRecord:

  @staticmethod
  def value_is_csv_exportable(value):
    return type(value) in (int, float, bool, complex, str) or isinstance(value, DataRecord) or isinstance(value, uint8)

  @classmethod
  def export_csv(cls, file_name):
    all_records = list(cls.all())
    with open(file_name, 'w') as export_file:
      field_names = []
      test_object = all_records[0].__dict__
      if hasattr(cls, 'CSV_EXPORT_FIELDS'):
        field_names = [field_name_for_csv_export_value(key, test_object.get(key, None)) for key in cls.CSV_EXPORT_FIELDS]
      else:
        field_names = [field_name_for_csv_export_value(key, test_object[key]) for key in test_object.keys() if DataRecord.value_is_csv_exportable(test_object[key])]
      writer = csv.DictWriter(export_file, fieldnames=field_names)
      writer.writeheader()
      for record in all_records:
        writer.writerow(record.as_csv_export_dict())

  @classmethod
  def get_store(cls):
    if hasattr(cls, 'store'):
      return cls.store
    cls.store = {}
    return cls.store

  @classmethod
  def count(cls):
    return len(cls.get_store().keys())

  @classmethod
  def all(cls):
    return cls.get_store().values()

  @classmethod
  def all_with(cls, filter_func):
    return list(filter(filter_func, cls.all()))

  @classmethod
  def find(cls, record_id):
    return cls.get_store().get(str(record_id), None)

  @classmethod
  def save(cls, record_id, record):
    cls.get_store()[str(record_id)] = record

  @classmethod
  def create_or_update(cls, record_id, **kwargs):
    found_record = cls.find(str(record_id))
    if found_record is not None:
      for name, value in kwargs.items():
        setattr(found_record, name, value)
      return found_record
    return cls(str(record_id), **kwargs)

  def __init__(self, record_id):
    self.record_id = str(record_id)
    self.__class__.save(str(record_id), self)

  def as_csv_export_dict(self):
    if hasattr(self.__class__, 'CSV_EXPORT_FIELDS'):
      return {field_name_for_csv_export_value(key, value): csv_export_value(value) for key, value in self.__dict__.items() if key in self.__class__.CSV_EXPORT_FIELDS}

    export_dict = {}
    for key in self.__dict__.keys():
      value_to_export = getattr(self, key)
      if DataRecord.value_is_csv_exportable(value_to_export):
        export_dict[field_name_for_csv_export_value(key, value_to_export)] = csv_export_value(value_to_export)
    return export_dict

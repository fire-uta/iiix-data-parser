from filterable import Filterable
from functools import reduce
import numpy


class HasDocuments:

  def __init__(self):
    self.seen_documents = {}
    self.viewed_documents = {}
    self.marked_relevant_documents = {}

  def add_seen_documents(self, *documents):
    for document in documents:
      self.seen_documents[ document.record_id ] = document

  def add_viewed_documents( self, *documents ):
    for document in documents:
      self.viewed_documents[ document.record_id ] = document

  def add_marked_relevant_documents( self, *documents ):
    for document in documents:
      self.marked_relevant_documents[ document.record_id ] = document

  def seen_highly_relevant_documents(self):
    return [document for document in self.seen_documents.values() if document.is_highly_relevant_for_topic( self.topic )]

  def seen_moderately_relevant_documents(self):
    return [document for document in self.seen_documents.values() if document.is_moderately_relevant_for_topic( self.topic )]

  def seen_non_relevant_documents(self):
    return [document for document in self.seen_documents.values() if not document.is_relevant_for_topic( self.topic )]

  def viewed_highly_relevant_documents(self):
    return [document for document in self.viewed_documents.values() if document.is_highly_relevant_for_topic( self.topic )]

  def viewed_moderately_relevant_documents(self):
    return [document for document in self.viewed_documents.values() if document.is_moderately_relevant_for_topic( self.topic )]

  def viewed_non_relevant_documents(self):
    return [document for document in self.viewed_documents.values() if not document.is_relevant_for_topic( self.topic )]

  def marked_highly_relevant_documents(self):
    return [document for document in self.marked_relevant_documents.values() if document.is_highly_relevant_for_topic( self.topic )]

  def marked_moderately_relevant_documents(self):
    return [document for document in self.marked_relevant_documents.values() if document.is_moderately_relevant_for_topic( self.topic )]

  def marked_non_relevant_documents(self):
    return [document for document in self.marked_relevant_documents.values() if not document.is_relevant_for_topic( self.topic )]

  def random_click_probability(self):
    if len(self.seen_documents) == 0:
      return 0
    return len(self.viewed_documents) / len(self.seen_documents)

  def amount_of_seen_documents(self):
    return len(self.seen_documents)

  @classmethod
  def amount_of_seen_highly_relevant_documents(cls, filter_func=Filterable.identity_filter, instances=None):
    if instances is None:
      instances = cls.get_store().values()
    return reduce(lambda acc, instance: acc + len(instance.seen_highly_relevant_documents()), list(filter(filter_func, instances)), 0)

  @classmethod
  def amount_of_seen_highly_relevant_documents_std(cls, filter_func=Filterable.identity_filter, instances=None):
    if instances is None:
      instances = cls.get_store().values()
    return numpy.std([len(instance.seen_highly_relevant_documents()) for instance in list(filter(filter_func, instances))])

  @classmethod
  def amount_of_viewed_highly_relevant_documents(cls, filter_func=Filterable.identity_filter, instances=None):
    if instances is None:
      instances = cls.get_store().values()
    return reduce(lambda acc, instance: acc + len(instance.viewed_highly_relevant_documents()), list(filter(filter_func, instances)), 0)

  @classmethod
  def amount_of_marked_highly_relevant_documents(cls, filter_func=Filterable.identity_filter, instances=None):
    if instances is None:
      instances = cls.get_store().values()
    return reduce(lambda acc, instance: acc + len(instance.marked_highly_relevant_documents()), list(filter(filter_func, instances)), 0)

  @classmethod
  def amount_of_marked_moderately_relevant_documents(cls, filter_func=Filterable.identity_filter, instances=None):
    if instances is None:
      instances = cls.get_store().values()
    return reduce(lambda acc, instance: acc + len(instance.marked_moderately_relevant_documents()), list(filter(filter_func, instances)), 0)

  @classmethod
  def amount_of_marked_non_relevant_documents(cls, filter_func=Filterable.identity_filter, instances=None):
    if instances is None:
      instances = cls.get_store().values()
    return reduce(lambda acc, instance: acc + len(instance.marked_non_relevant_documents()), list(filter(filter_func, instances)), 0)

  @classmethod
  def amount_of_seen_moderately_relevant_documents(cls, filter_func=Filterable.identity_filter, instances=None):
    if instances is None:
      instances = cls.get_store().values()
    return reduce(lambda acc, instance: acc + len(instance.seen_moderately_relevant_documents()), list(filter(filter_func, instances)), 0)

  @classmethod
  def amount_of_viewed_moderately_relevant_documents(cls, filter_func=Filterable.identity_filter, instances=None):
    if instances is None:
      instances = cls.get_store().values()
    return reduce(lambda acc, instance: acc + len(instance.viewed_moderately_relevant_documents()), list(filter(filter_func, instances)), 0)

  @classmethod
  def amount_of_seen_non_relevant_documents(cls, filter_func=Filterable.identity_filter, instances=None):
    if instances is None:
      instances = cls.get_store().values()
    return reduce(lambda acc, instance: acc + len(instance.seen_non_relevant_documents()), list(filter(filter_func, instances)), 0)

  @classmethod
  def amount_of_viewed_non_relevant_documents(cls, filter_func=Filterable.identity_filter, instances=None):
    if instances is None:
      instances = cls.get_store().values()
    return reduce(lambda acc, instance: acc + len(instance.viewed_non_relevant_documents()), list(filter(filter_func, instances)), 0)

  @classmethod
  def average_random_click_probability(cls, filter_func=Filterable.identity_filter, records=None):
    if records is None:
      records = cls.all_with(filter_func)
    return numpy.mean([record.random_click_probability() for record in records])

  @classmethod
  def ratio_of_seen_documents_at_rank(cls, rank, filter_func=Filterable.identity_filter, records=None):
    if records is None:
      records = cls.all_with(filter_func)
    records_with_enough_seen_docs = list(filter(lambda record: record.amount_of_seen_documents() >= rank, records))
    return float(len(records_with_enough_seen_docs)) / float(len(records))

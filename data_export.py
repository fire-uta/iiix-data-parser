import csv


import numpy


from result_file import ResultFile
from queries_summary_file import QueriesSummaryFile
from log_file import LogFile
from combined_log_file import CombinedLogFile
from document import Document
from query import Query
from topic import Topic
from user import User
from condition import Condition
from action import Action
from session import Session
from relevance import Relevance
from filterable import Filterable
from session_time_slice import SessionTimeSlice


def export_read_events_as_csv(sessions, file_name, gains):
  with open(file_name, 'w') as export_file:
    field_names = ['session_id', 'topic', 'condition', 'document_id', 'relevance', 'read_start_at', 'read_duration',
                   'gain_at_read_start', 'marked?', 'marked_at', 'rank', 'continuous_rank', 'query_order_num',
                   'cumulated_read_count_nr_inc1', 'cumulated_read_count_nr_inc2+',
                   'cumulated_read_count_r_inc1', 'cumulated_read_count_r_inc2+',
                   'cumulated_scan_count_nr_inc1', 'cumulated_scan_count_nr_inc2+',
                   'cumulated_scan_count_r_inc1', 'cumulated_scan_count_r_inc2+',
                   'document_incidence', 'read_incidence', 'read_incidence_unique']
    writer = csv.DictWriter(export_file, fieldnames=field_names)
    writer.writeheader()
    for session in sessions:
      for read_event in session.document_read_events():
        result = read_event['result']
        writer.writerow({
            'session_id': session.record_id,
            'topic': session.topic.record_id,
            'condition': session.condition.record_id,
            'document_id': read_event['document'].record_id,
            'read_start_at': read_event['read_start_at_seconds'],
            'read_duration': read_event['read_duration'],
            'relevance': read_event['document'].get_relevance_for_topic(session.topic).relevance_level,
            'gain_at_read_start': session.cumulated_gain_at(read_event['read_start_at_seconds'], gains),
            'marked?': ((1 if result.has_been_marked() else 0) if result is not None else None),
            'marked_at': (result.mark_start_at_from_session_start_seconds() if result is not None else None),
            'rank': read_event['rank'],
            'continuous_rank': read_event['continuous_rank'],
            'query_order_num': read_event['query_order_number'],
            'cumulated_read_count_nr_inc1': session.cumulated_read_count_at(read_event['read_start_at_seconds'], relevance_level_match=lambda r: r == 0, incidence_match=lambda i: i == 1),
            'cumulated_read_count_nr_inc2+': session.cumulated_read_count_at(read_event['read_start_at_seconds'], relevance_level_match=lambda r: r == 0, incidence_match=lambda i: i >= 2),
            'cumulated_read_count_r_inc1': session.cumulated_read_count_at(read_event['read_start_at_seconds'], relevance_level_match=lambda r: r >= 1, incidence_match=lambda i: i == 1),
            'cumulated_read_count_r_inc2+': session.cumulated_read_count_at(read_event['read_start_at_seconds'], relevance_level_match=lambda r: r >= 1, incidence_match=lambda i: i >= 2),
            'cumulated_scan_count_nr_inc1': session.results_count_at_rank(read_event['continuous_rank'], relevance_level_match=lambda r: r == 0, incidence_match=lambda i: i == 1),
            'cumulated_scan_count_nr_inc2+': session.results_count_at_rank(read_event['continuous_rank'], relevance_level_match=lambda r: r == 0, incidence_match=lambda i: i >= 2),
            'cumulated_scan_count_r_inc1': session.results_count_at_rank(read_event['continuous_rank'], relevance_level_match=lambda r: r >= 1, incidence_match=lambda i: i == 1),
            'cumulated_scan_count_r_inc2+': session.results_count_at_rank(read_event['continuous_rank'], relevance_level_match=lambda r: r >= 1, incidence_match=lambda i: i >= 2),
            'document_incidence': read_event['document_incidence'],
            'read_incidence': read_event['read_incidence'],
            'read_incidence_unique': read_event['read_incidence_unique']
        })


def export_query_formulation_events_as_csv(sessions, file_name, gains):
  with open(file_name, 'w') as export_file:
    field_names = ['session_id', 'topic', 'condition', 'query_formulation_start_at', 'query_formulation_duration',
                   'gain_at_query_formulation_start', 'total_query_duration', 'average_snippet_scan_duration',
                   'query_order_nr', 'autocomplete', 'map', 'query_text']
    writer = csv.DictWriter(export_file, fieldnames=field_names)
    writer.writeheader()
    for session in sessions:
      for query_formulation_event in session.query_formulation_events():
        query_formulation_start_at = query_formulation_event['query_formulation_start_at']
        precision = query_formulation_event['precision']
        writer.writerow({
            'session_id': session.record_id,
            'topic': session.topic.record_id,
            'condition': session.condition.record_id,
            'query_formulation_start_at': query_formulation_start_at,
            'query_formulation_duration': query_formulation_event['query_formulation_duration'],
            'gain_at_query_formulation_start': session.cumulated_gain_at(query_formulation_start_at, gains) if query_formulation_start_at is not None else None,
            'autocomplete': query_formulation_event['autocomplete'],
            'map': precision['map'] if precision is not None else None,
            'query_text': query_formulation_event['query_text'],
            'average_snippet_scan_duration': query_formulation_event['average_snippet_scan_duration'],
            'query_order_nr': query_formulation_event['query_order_number'],
            'total_query_duration': query_formulation_event['duration_in_seconds']
        })


def export_marked_relevant_events_as_csv(sessions, file_name, gains):
  with open(file_name, 'w') as export_file:
    field_names = ['session_id', 'topic', 'condition', 'document_id', 'relevance', 'mark_start_at', 'mark_duration',
                   'gain_before_mark_start', 'rank', 'continuous_rank', 'query_order_nr',
                   'cumulated_mark_count_nr_inc1', 'cumulated_mark_count_nr_inc2+',
                   'cumulated_mark_count_r_inc1', 'cumulated_mark_count_r_inc2+',
                   'cumulated_read_count_nr_inc1', 'cumulated_read_count_nr_inc2+',
                   'cumulated_read_count_r_inc1', 'cumulated_read_count_r_inc2+',
                   'document_incidence', 'read_incidence', 'mark_incidence',
                   'read_incidence_unique', 'mark_incidence_unique']
    writer = csv.DictWriter(export_file, fieldnames=field_names)
    writer.writeheader()
    for session in sessions:
      for mark_event in session.document_marked_relevant_events():
        writer.writerow({
            'session_id': session.record_id,
            'topic': session.topic.record_id,
            'condition': session.condition.record_id,
            'document_id': mark_event['document'].record_id,
            'mark_start_at': mark_event['mark_start_at_seconds'],
            'mark_duration': mark_event['mark_duration'],
            'relevance': mark_event['document'].get_relevance_for_topic(session.topic).relevance_level,
            'gain_before_mark_start': session.cumulated_gain_at(mark_event['mark_start_at_seconds'] - 1, gains),
            'rank': mark_event['rank'],
            'continuous_rank': mark_event['continuous_rank'],
            'query_order_nr': mark_event['query_order_number'],
            'cumulated_mark_count_nr_inc1': session.cumulated_mark_count_at(mark_event['mark_start_at_seconds'], relevance_level_match=lambda r: r == 0, incidence_match=lambda i: i == 1),
            'cumulated_mark_count_nr_inc2+': session.cumulated_mark_count_at(mark_event['mark_start_at_seconds'], relevance_level_match=lambda r: r == 0, incidence_match=lambda i: i >= 2),
            'cumulated_mark_count_r_inc1': session.cumulated_mark_count_at(mark_event['mark_start_at_seconds'], relevance_level_match=lambda r: r >= 1, incidence_match=lambda i: i == 1),
            'cumulated_mark_count_r_inc2+': session.cumulated_mark_count_at(mark_event['mark_start_at_seconds'], relevance_level_match=lambda r: r >= 1, incidence_match=lambda i: i >= 2),
            'cumulated_read_count_nr_inc1': session.cumulated_read_count_at(mark_event['mark_start_at_seconds'], relevance_level_match=lambda r: r == 0, incidence_match=lambda i: i == 1),
            'cumulated_read_count_nr_inc2+': session.cumulated_read_count_at(mark_event['mark_start_at_seconds'], relevance_level_match=lambda r: r == 0, incidence_match=lambda i: i >= 2),
            'cumulated_read_count_r_inc1': session.cumulated_read_count_at(mark_event['mark_start_at_seconds'], relevance_level_match=lambda r: r >= 1, incidence_match=lambda i: i == 1),
            'cumulated_read_count_r_inc2+': session.cumulated_read_count_at(mark_event['mark_start_at_seconds'], relevance_level_match=lambda r: r >= 1, incidence_match=lambda i: i >= 2),
            'document_incidence': mark_event['document_incidence'],
            'read_incidence': mark_event['read_incidence'],
            'mark_incidence': mark_event['mark_incidence'],
            'read_incidence_unique': mark_event['read_incidence_unique'],
            'mark_incidence_unique': mark_event['mark_incidence_unique']
        })


def export_scanned_documents_as_csv(sessions, file_name, gains):
  with open(file_name, 'w') as export_file:
    field_names = ['session_id', 'topic', 'condition', 'query_id', 'rank', 'document_id', 'relevance', 'clicked?',
                   'marked?', 'first_encountered', 'clicked_at', 'marked_at',
                   'continuous_rank', 'query_order_nr', 'gain_after_marking', 'cumulated_scan_count_nr_inc1',
                   'cumulated_scan_count_nr_inc2+', 'cumulated_scan_count_r_inc1', 'cumulated_scan_count_r_inc2+',
                   'cumulated_read_count_before_nr', 'cumulated_read_count_before_r',
                   'cumulated_mark_count_before_nr', 'cumulated_mark_count_before_r', 'document_incidence']
    writer = csv.DictWriter(export_file, fieldnames=field_names)
    writer.writeheader()
    for session in sessions:
      for query in session.queries.values():
        for result_document in query.result_list.results_up_to_last_rank_reached():
          document = result_document.document
          continuous_rank = query.continuous_rank_at(result_document.rank)
          relevance = None
          try:
            relevance = document.get_relevance_for_topic(session.topic)
          except:
            raise RuntimeError("Relevance not found: docid %s, topic id %s, query id %s, session id %s" % (document.record_id, session.topic.record_id, query.record_id, session.record_id))
          writer.writerow({
              'session_id': session.record_id,
              'topic': session.topic.record_id,
              'condition': session.condition.record_id,
              'query_id': query.record_id,
              'rank': result_document.rank,
              'document_id': document.record_id,
              'relevance': relevance.relevance_level if relevance is not None else None,
              'marked?': (1 if result_document.has_been_marked() else 0),
              'clicked?': (1 if result_document.has_been_viewed() else 0),
              'first_encountered': result_document.first_encountered_at_from_session_start_seconds(),
              'clicked_at': result_document.read_start_at_from_session_start_seconds(),
              'marked_at': result_document.mark_start_at_from_session_start_seconds(),
              'continuous_rank': continuous_rank,
              'query_order_nr': query.order_number(),
              'gain_after_marking': (session.cumulated_gain_at(result_document.mark_start_at_from_session_start_seconds() + 1, gains) if query.has_been_marked(document) else None),
              'cumulated_scan_count_nr_inc1': session.results_count_at_rank(continuous_rank, relevance_level_match=lambda r: r == 0, incidence_match=lambda i: i == 1),
              'cumulated_scan_count_nr_inc2+': session.results_count_at_rank(continuous_rank, relevance_level_match=lambda r: r == 0, incidence_match=lambda i: i >= 2),
              'cumulated_scan_count_r_inc1': session.results_count_at_rank(continuous_rank, relevance_level_match=lambda r: r >= 1, incidence_match=lambda i: i == 1),
              'cumulated_scan_count_r_inc2+': session.results_count_at_rank(continuous_rank, relevance_level_match=lambda r: r >= 1, incidence_match=lambda i: i >= 2),
              'cumulated_read_count_before_nr': session.cumulated_read_count_before_rank(continuous_rank, relevance_level_match=lambda r: r == 0),
              'cumulated_read_count_before_r': session.cumulated_read_count_before_rank(continuous_rank, relevance_level_match=lambda r: r >= 1),
              'cumulated_mark_count_before_nr': session.cumulated_mark_count_before_rank(continuous_rank, relevance_level_match=lambda r: r == 0),
              'cumulated_mark_count_before_r': session.cumulated_mark_count_before_rank(continuous_rank, relevance_level_match=lambda r: r >= 1),
              'document_incidence': session.incidence_of(document, query)
          })


def export_actions(reject_groups, gains):
  for name, group in reject_groups.items():
    full_filter = Filterable.combine_filters(Filterable.user_filter(*group['users']),
                                             Filterable.practice_topic_reject_filter)
    export_scanned_documents_as_csv(Session.filtered_records(full_filter), name + '_scanned_documents.csv', gains)
    export_read_events_as_csv(Session.filtered_records(full_filter), name + '_read_events.csv', gains)
    export_marked_relevant_events_as_csv(Session.filtered_records(full_filter), name + '_marked_relevant_events.csv', gains)
    export_query_formulation_events_as_csv(Session.filtered_records(full_filter), name + '_query_formulation_events.csv', gains)


def export_entities():
  Query.export_csv('all_queries.csv')
  Action.export_csv('all_actions.csv')
  Condition.export_csv('all_conditions.csv')
  Document.export_csv('all_documents.csv')
  Relevance.export_csv('all_relevances.csv')
  Session.export_csv('all_sessions.csv')
  Topic.export_csv('all_topics.csv')
  User.export_csv('all_users.csv')

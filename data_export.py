def export_read_events_as_csv(sessions, file_name):
  with open(file_name, 'w') as export_file:
    field_names = ['session_id', 'topic', 'condition', 'document_id', 'relevance', 'read_start_at', 'read_duration', 'gain_at_read_start', 'marked?', 'marked_at', 'rank', 'continuous_rank', 'query_order_nr', 'cumulated_read_count_0', 'cumulated_read_count_1', 'cumulated_read_count_2', 'cumulated_scan_count_0', 'cumulated_scan_count_1', 'cumulated_scan_count_2']
    writer = csv.DictWriter(export_file, fieldnames=field_names)
    writer.writeheader()
    for session in sessions:
      for read_event in session.document_read_events():
        writer.writerow({
            'session_id': session.record_id,
            'topic': session.topic.record_id,
            'condition': session.condition.record_id,
            'document_id': read_event['document'].record_id,
            'read_start_at': read_event['read_start_at_seconds'],
            'read_duration': read_event['read_duration'],
            'relevance': read_event['document'].get_relevance_for_topic(session.topic).relevance_level,
            'gain_at_read_start': session.cumulated_gain_at(read_event['read_start_at_seconds'], gains),
            'marked?': (1 if session.has_been_marked(read_event['document']) else 0),
            'marked_at': session.document_mark_start_at_seconds(read_event['document']),
            'rank': read_event['rank'],
            'continuous_rank': read_event['continuous_rank'],
            'query_order_nr': read_event['query_order_number'],
            'cumulated_read_count_0': session.cumulated_non_relevant_read_count_at(read_event['read_start_at_seconds']),
            'cumulated_read_count_1': session.cumulated_moderately_relevant_read_count_at(read_event['read_start_at_seconds']),
            'cumulated_read_count_2': session.cumulated_highly_relevant_read_count_at(read_event['read_start_at_seconds']),
            'cumulated_scan_count_0': session.non_relevant_results_count_at_rank(read_event['continuous_rank']),
            'cumulated_scan_count_1': session.moderately_relevant_results_count_at_rank(read_event['continuous_rank']),
            'cumulated_scan_count_2': session.highly_relevant_results_count_at_rank(read_event['continuous_rank'])
        })


def export_query_formulation_events_as_csv(sessions, file_name):
  with open(file_name, 'w') as export_file:
    field_names = ['session_id', 'topic', 'condition', 'query_formulation_start_at', 'query_formulation_duration', 'gain_at_query_formulation_start', 'total_query_duration', 'average_snippet_scan_duration', 'query_order_nr', 'autocomplete', 'map', 'query_text']
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


def export_marked_relevant_events_as_csv(sessions, file_name):
  with open(file_name, 'w') as export_file:
    field_names = ['session_id', 'topic', 'condition', 'document_id', 'relevance', 'mark_start_at', 'mark_duration', 'gain_before_mark_start', 'rank', 'continuous_rank', 'query_order_nr', 'cumulated_mark_count_0', 'cumulated_mark_count_1', 'cumulated_mark_count_2', 'cumulated_read_count_0', 'cumulated_read_count_1', 'cumulated_read_count_2']
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
            'cumulated_mark_count_0': session.cumulated_non_relevant_mark_count_at(mark_event['mark_start_at_seconds']),
            'cumulated_mark_count_1': session.cumulated_moderately_relevant_mark_count_at(mark_event['mark_start_at_seconds']),
            'cumulated_mark_count_2': session.cumulated_highly_relevant_mark_count_at(mark_event['mark_start_at_seconds']),
            'cumulated_read_count_0': session.cumulated_non_relevant_read_count_at(mark_event['mark_start_at_seconds']),
            'cumulated_read_count_1': session.cumulated_moderately_relevant_read_count_at(mark_event['mark_start_at_seconds']),
            'cumulated_read_count_2': session.cumulated_highly_relevant_read_count_at(mark_event['mark_start_at_seconds'])
        })


def export_scanned_documents_as_csv(sessions, file_name):
  with open(file_name, 'w') as export_file:
    field_names = ['session_id', 'topic', 'condition', 'query_id', 'rank', 'document_id', 'relevance', 'clicked?', 'marked?', 'first_encountered', 'clicked_at', 'marked_at', 'continuous_rank', 'query_order_nr', 'gain_after_marking', 'cumulated_scan_count_0', 'cumulated_scan_count_1', 'cumulated_scan_count_2']
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
              'marked?': (1 if query.has_been_marked(document) else 0),
              'clicked?': (1 if query.has_been_viewed(document) else 0),
              'first_encountered': result_document.first_encountered_at_from_session_start_seconds(),
              'clicked_at': result_document.read_start_at_from_session_start_seconds(),
              'marked_at': result_document.mark_start_at_from_session_start_seconds(),
              'continuous_rank': continuous_rank,
              'query_order_nr': query.order_number(),
              'gain_after_marking': (session.cumulated_gain_at(result_document.mark_start_at_from_session_start_seconds() + 1, gains) if query.has_been_marked(document) else None),
              'cumulated_scan_count_0': session.non_relevant_results_count_at_rank(continuous_rank),
              'cumulated_scan_count_1': session.moderately_relevant_results_count_at_rank(continuous_rank),
              'cumulated_scan_count_2': session.highly_relevant_results_count_at_rank(continuous_rank)
          })


def export_actions(reject_groups):
  for name, group in reject_groups.items():
    full_filter = Filterable.combine_filters(Filterable.user_filter(*group['users']),
                                             Filterable.practice_topic_reject_filter)
    export_scanned_documents_as_csv(Session.filtered_records(full_filter), name + '_scanned_documents.csv')
    export_read_events_as_csv(Session.filtered_records(full_filter), name + '_read_events.csv')
    export_marked_relevant_events_as_csv(Session.filtered_records(full_filter), name + '_marked_relevant_events.csv')
    export_query_formulation_events_as_csv(Session.filtered_records(full_filter), name + '_query_formulation_events.csv')


def export_entities():
  Query.export_csv('all_queries.csv')
  Action.export_csv('all_actions.csv')
  Condition.export_csv('all_conditions.csv')
  Document.export_csv('all_documents.csv')
  Relevance.export_csv('all_relevances.csv')
  Session.export_csv('all_sessions.csv')
  Topic.export_csv('all_topics.csv')
  User.export_csv('all_users.csv')

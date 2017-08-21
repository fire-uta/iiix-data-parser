def print_session_time_slice_click_stats_for_filter(fil, time_slices):
  (seen_h, viewed_h, marked_h) = (SessionTimeSlice.amount_of_seen_highly_relevant_documents(fil, time_slices),
    SessionTimeSlice.amount_of_viewed_highly_relevant_documents(fil, time_slices),
    SessionTimeSlice.amount_of_marked_highly_relevant_documents(fil, time_slices))
  print('Highly relevant docs seen across time slices: %i, of which viewed: %i (%f), of which marked relevant: %i (%f)' % (
    seen_h, viewed_h, float(viewed_h)/float(seen_h), marked_h, float(marked_h)/float(viewed_h) ))

  (seen_m, viewed_m, marked_m) = (SessionTimeSlice.amount_of_seen_moderately_relevant_documents(fil, time_slices),
    SessionTimeSlice.amount_of_viewed_moderately_relevant_documents(fil, time_slices),
    SessionTimeSlice.amount_of_marked_moderately_relevant_documents(fil, time_slices))
  print("Moderately relevant docs seen across time slices: %i, of which viewed: %i (%f), of which marked relevant: %i (%f)" % (
    seen_m, viewed_m, float(viewed_m)/float(seen_m), marked_m, float(marked_m)/float(viewed_m) ))

  (seen_n, viewed_n, marked_n) = (SessionTimeSlice.amount_of_seen_non_relevant_documents(fil, time_slices),
    SessionTimeSlice.amount_of_viewed_non_relevant_documents(fil, time_slices),
    SessionTimeSlice.amount_of_marked_non_relevant_documents(fil, time_slices))
  print("Non-relevant docs seen across time slices: %i, of which viewed: %i (%f), of which marked relevant: %i (%f)" % (
    seen_n, viewed_n, float(viewed_n)/float(seen_n), marked_n, float(marked_n)/float(viewed_n) ))


def print_session_stats_for_filter(fil):
  (seen_h, viewed_h, marked_h) = (Session.amount_of_seen_highly_relevant_documents( fil ),
    Session.amount_of_viewed_highly_relevant_documents( fil ),
    Session.amount_of_marked_highly_relevant_documents( fil ))
  print('Highly relevant docs seen across sessions: %i, of which viewed: %i (%f), of which marked relevant: %i (%f)' % (
    seen_h, viewed_h, float(viewed_h)/float(seen_h), marked_h, float(marked_h)/float(viewed_h) ))

  (seen_m, viewed_m, marked_m) = (Session.amount_of_seen_moderately_relevant_documents(fil),
    Session.amount_of_viewed_moderately_relevant_documents(fil),
    Session.amount_of_marked_moderately_relevant_documents(fil))
  print("Moderately relevant docs seen across sessions: %i, of which viewed: %i (%f), of which marked relevant: %i (%f)" % (
    seen_m, viewed_m, float(viewed_m)/float(seen_m), marked_m, float(marked_m)/float(viewed_m) ))

  (seen_n, viewed_n, marked_n) = (Session.amount_of_seen_non_relevant_documents(fil),
    Session.amount_of_viewed_non_relevant_documents(fil),
    Session.amount_of_marked_non_relevant_documents(fil))
  print("Non-relevant docs seen across sessions: %i, of which viewed: %i (%f), of which marked relevant: %i (%f)" % (
    seen_n, viewed_n, float(viewed_n)/float(seen_n), marked_n, float(marked_n)/float(viewed_n) ))


def print_query_stats_for_filter(fil):
  (seen_qh, viewed_qh, marked_qh) = (Query.amount_of_seen_highly_relevant_documents( fil ),
    Query.amount_of_viewed_highly_relevant_documents( fil ),
    Query.amount_of_marked_highly_relevant_documents( fil ))
  print("Highly relevant unique docs seen across queries: %i, of which viewed: %i (%f), of which marked relevant: %i (%f) (marked relevant / seen: %f)" % (
    seen_qh, viewed_qh, float(viewed_qh)/float(seen_qh), marked_qh, float(marked_qh)/float(viewed_qh), float(marked_qh)/float(seen_qh) ))

  (seen_qm, viewed_qm, marked_qm) = (Query.amount_of_seen_moderately_relevant_documents(fil),
    Query.amount_of_viewed_moderately_relevant_documents(fil),
    Query.amount_of_marked_moderately_relevant_documents(fil))
  print("Moderately relevant unique docs seen across queries: %i, of which viewed: %i (%f), of which marked relevant: %i (%f) (marked relevant / seen: %f)" % (
    seen_qm, viewed_qm, float(viewed_qm)/float(seen_qm), marked_qm, float(marked_qm)/float(viewed_qm), float(marked_qm)/float(seen_qm) ))

  (seen_qn, viewed_qn, marked_qn) = (Query.amount_of_seen_non_relevant_documents(fil),
    Query.amount_of_viewed_non_relevant_documents(fil),
    Query.amount_of_marked_non_relevant_documents(fil))
  print("Non-relevant unique docs seen across queries: %i, of which viewed: %i (%f), of which marked relevant: %i (%f) (marked relevant / seen: %f)" % (
    seen_qn, viewed_qn, float(viewed_qn)/float(seen_qn), marked_qn, float(marked_qn)/float(viewed_qn), float(marked_qn)/float(seen_qn) ))


def print_session_time_slice_stats_for_filter(fil, time_slices):
  print_session_time_slice_click_stats_for_filter(fil, time_slices)

  print("Average document reading time: %s sec (median: %s sec, std: %s sec)" %
        (SessionTimeSlice.average_document_reading_time_in_seconds_over(time_slices),
         SessionTimeSlice.median_document_reading_time_in_seconds_over(time_slices),
         SessionTimeSlice.std_document_reading_time_in_seconds_over(time_slices)))
  print("Average query formulation time: %s sec (median: %s sec, std: %s sec)" %
        (SessionTimeSlice.average_query_formulation_time_in_seconds_over(time_slices),
         SessionTimeSlice.median_query_formulation_time_in_seconds_over(time_slices),
         SessionTimeSlice.std_query_formulation_time_in_seconds_over(time_slices)))
  print("Average total query time: %s sec (median: %s sec, std: %s sec)" %
        (SessionTimeSlice.average_total_query_duration_over(time_slices),
         SessionTimeSlice.median_total_query_duration_over(time_slices),
         SessionTimeSlice.std_total_query_duration_over(time_slices)))
  print("Average snippet scanning time: %s sec" %
        SessionTimeSlice.average_snippet_scanning_time_in_seconds_over(time_slices))
  print("Average query last rank reached: %s (median: %s, std: %s)" %
        (SessionTimeSlice.average_last_rank_reached_over(time_slices),
         SessionTimeSlice.median_last_rank_reached_over(time_slices),
         SessionTimeSlice.std_last_rank_reached_over(time_slices)))
  print("Average amount of non-relevant docs seen when stopping: %s (median: %s, std: %s)" %
        (SessionTimeSlice.average_amount_of_non_relevant_documents_seen_at_last_rank_over(time_slices),
         SessionTimeSlice.median_amount_of_non_relevant_documents_seen_at_last_rank_over(time_slices),
         SessionTimeSlice.std_amount_of_non_relevant_documents_seen_at_last_rank_over(time_slices)))
  print("Average amount of contiguous non-relevant docs seen when stopping: %s (median: %s, std: %s)" %
        (SessionTimeSlice.average_amount_of_contiguous_non_relevant_documents_seen_at_last_rank_over(time_slices),
         SessionTimeSlice.median_amount_of_contiguous_non_relevant_documents_seen_at_last_rank_over(time_slices),
         SessionTimeSlice.std_amount_of_contiguous_non_relevant_documents_seen_at_last_rank_over(time_slices)))
  print("Average random click probability: %s (median: %s, std: %s)" %
        (SessionTimeSlice.average_random_click_probability_over(time_slices),
         SessionTimeSlice.median_random_click_probability_over(time_slices),
         SessionTimeSlice.std_random_click_probability_over(time_slices)))


  for rank in range(0, 21):
    print("Rank %s examine probability: %s" %
          (rank, SessionTimeSlice.average_ratio_of_seen_documents_at_rank_over(rank, time_slices)))


def print_stats_for_filter(fil):
  print_session_stats_for_filter( fil )
  print_query_stats_for_filter( fil )

  print("Average document reading time: %s sec" % Session.global_average_document_reading_time_in_seconds( fil ))
  print("Average query formulation time: %s sec" % Query.average_formulation_time_in_seconds( fil ))
  print("Average snippet scanning time: %s sec" % Session.global_average_snippet_scanning_time_in_seconds( fil ))
  print("Average query last rank reached: %s" % Query.average_last_rank_reached( fil ))
  print("Average amount of non-relevant docs seen when stopping: %s" % Query.average_amount_of_non_relevant_documents_seen_at_last_rank( fil ))
  print("Average amount of contiguous non-relevant docs seen when stopping: %s" % Query.average_amount_of_contiguous_non_relevant_documents_seen_at_last_rank( fil ))
  print("Average random click probability: %s" % Session.average_random_click_probability(fil))

  for rank in range(0, 51):
    print("Rank %s examine probability: %s" % (rank, Query.ratio_of_seen_documents_at_rank(rank, fil)))


def output_gain_statistics(fil, filename, gains):
  sessions = Session.filtered_records(fil)
  fields = range(0,1300,10)

  with open(filename, 'w') as output_file:
    writer = csv.DictWriter( output_file, fieldnames = ['session_id'] + fields )
    writer.writeheader()
    for session in sessions:
      row = {'session_id': session.record_id}
      for secs in fields:
        row[secs] = session.cumulated_gain_at( secs, gains )
      writer.writerow( row )


def output_doc_statistics(sessions, filename, marked=False):
  fields = list(range(0, 1300, 10))
  with open(filename, 'w') as output_file:
    writer = csv.DictWriter(output_file, fieldnames=['session_id', 'topic_id', 'condition'] + fields)
    writer.writeheader()
    for session in sessions:
      row = {'session_id': session.record_id, 'topic_id': session.topic.record_id, 'condition': session.condition.record_id}
      for secs in fields:
        row[secs] = session.marked_documents_count_at(secs) if marked else session.viewed_documents_count_at(secs)
      writer.writerow(row)


def output_seen_doc_statistics(time_slices, filename, seconds_between=240):
  fields = list(range(seconds_between, 1300, seconds_between))
  with open(filename, 'w') as output_file:
    writer = csv.DictWriter(output_file, fieldnames=['session_id', 'topic_id', 'condition'] + fields)
    writer.writeheader()
    for single_session_slices in time_slices:
      parent_session = single_session_slices[0].session
      row = {'session_id': parent_session.record_id, 'topic_id': parent_session.topic.record_id, 'condition': parent_session.condition.record_id}
      cumulative_snippet_count = 0
      for time_slice in single_session_slices:
        end_secs = int((time_slice.start_msecs + time_slice.length_msecs) / 1000)
        cumulative_snippet_count += len(time_slice.seen_documents)
        row[end_secs] = cumulative_snippet_count
      writer.writerow(row)


def get_session_time_slices(fil, minutes=[0, 4, 8, 12, 16], length=4):
  sessions = Session.filtered_records(fil)
  all_time_slices = []
  for session in sessions:
    this_session_time_slices = []
    for i in minutes:
      start_msecs = i * 60 * 1000
      length_msecs = length * 60 * 1000
      previous_slice = this_session_time_slices[-1] if len(this_session_time_slices) > 0 else None
      this_session_time_slices.append(SessionTimeSlice(session, start_msecs, length_msecs, previous_slice))
    all_time_slices.append(this_session_time_slices)
  return all_time_slices


def print_time_slice_stats_for_filter(fil):
  all_time_slices = get_session_time_slices(fil)
  vertical_slices = zip(*all_time_slices)
  start_mins = 0
  for slices in vertical_slices:
    start_msecs = start_mins * 60 * 1000
    length_msecs = 4 * 60 * 1000
    print('Time slice stats, starting at %i msecs, ending after %i msecs' % (start_msecs, length_msecs))
    print_session_time_slice_stats_for_filter(fil, slices)
    start_mins = start_mins + 4

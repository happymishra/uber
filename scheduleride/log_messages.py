class LogMessage:
    REQUEST_UBER_API_LOG = "{date_time}: Requested uber api for {email}"
    REQUEST_MAP_API_LOG = "{date_time}: Requested Google maps api for {email}"
    UBER_BOOKED_LOG = "{date_time}: {email} - Cab booked with Uber coming in {uber_time}"
    LOG_DB_DATA = "{trip_id}, {email}, {time_to_reach_dest}, {tf}, {current_pt}"

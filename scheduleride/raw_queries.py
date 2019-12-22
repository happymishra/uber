TRIPS_TO_CHECK_QUERY = '''
    SELECT id, source, destination, time_to_reach_dest, email, ride_time,
            frequency, pending_time, traffic_time
    FROM scheduled_trip
    WHERE (CAST(strftime('%s', time_to_reach_dest) as integer) - 
            CAST(strftime('%s', DATETIME(CURRENT_TIMESTAMP, 'LOCALTIME')) as integer) < ride_time + {variation_time} + {uber_time} 
                AND frequency = 0)
        || (frequency = 2)
        || (frequency = 1 and (CAST(strftime('%s', time_to_reach_dest) as integer) - 
                                CAST(strftime('%s', DATETIME(CURRENT_TIMESTAMP, 'LOCALTIME')) as integer)) 
                                    < (pending_time / 2) + ride_time)
'''

UPDATE_TRIP_DETAILS_QUERY = '''
    UPDATE scheduled_trip
    SET frequency = {frequency},
        traffic_time = {ride_time},
        pending_time = {pending_time}
    where id = {trip_id}
'''

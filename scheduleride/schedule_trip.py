import logging
import sys
from datetime import datetime

from django.conf import settings

from scheduleride.email import Mail
from scheduleride.log_messages import LogMessage
from scheduleride.raw_queries import TRIPS_TO_CHECK_QUERY, UPDATE_TRIP_DETAILS_QUERY
from utils import ExecRawQuery, Cab, GoogleMaps

logger = logging.getLogger('custom-module')


class ScheduleTrip:
    def __int__(self):
        pass

    @staticmethod
    def get_all_ride_to_schedule():
        query = TRIPS_TO_CHECK_QUERY.format(variation_time=settings.MAX_VARIATION_TIME_POSSIBLE,
                                            uber_time=settings.UBER_TIME)

        return ExecRawQuery.select_raw_query(query)

    @staticmethod
    def get_nearest_cab(response, email, source):
        nearest_uber_time = sys.maxsize

        for i in range(3):
            response.append(LogMessage.REQUEST_UBER_API_LOG.format(date_time=datetime.now(),
                                                                   email=email))
            uber_time = Cab.get_uber(source)

            if uber_time < nearest_uber_time:
                nearest_uber_time = uber_time

        return nearest_uber_time

    @staticmethod
    def book_uber(response, email, source):
        nearest_uber = ScheduleTrip.get_nearest_cab(response, email, source)
        response.append(LogMessage.UBER_BOOKED_LOG.format(date_time=datetime.now(),
                                                          email=email,
                                                          uber_time=nearest_uber))

        Mail.send_email("Time to Book uber", "Kindly book your uber now!",
                        settings.EMAIL_HOST_USER, [email])

    @staticmethod
    def update_trip_details(ride_time, traffic_time, pending_time, trip_id):
        frequency = 1
        if ride_time - traffic_time > settings.ERROR_MARGIN_TIME:
            frequency = 2

        logger.info(f"Updating ride time: freq: {frequency} ride_time: {ride_time}, "
                    f"traffic_time: {traffic_time}")

        query = UPDATE_TRIP_DETAILS_QUERY.format(frequency=frequency, ride_time=ride_time,
                                                 pending_time=pending_time, trip_id=trip_id)
        ExecRawQuery.execute(query)

    @staticmethod
    def get_all_ride_details():
        response = list()
        trips = ScheduleTrip.get_all_ride_to_schedule()

        for each_trip in trips:
            trip_id = each_trip.get('id')
            email = each_trip.get('email')
            source = each_trip.get('source')
            destination = each_trip.get('destination')
            time_to_reach_dest = each_trip.get('time_to_reach_dest')
            traffic_time = each_trip.get('traffic_time')
            current_pending_time = time_to_reach_dest - datetime.now()

            logger.info(LogMessage.LOG_DB_DATA.format(trip_id=trip_id, email=email,
                                                      time_to_reach_dest=time_to_reach_dest,
                                                      tf=traffic_time,
                                                      current_pt=current_pending_time))

            source = [float(x) for x in source.split(',')]
            destination = [float(x) for x in destination.split(',')]
            ride_time = GoogleMaps.get_dynamic_ride_time(source, destination)

            response.append(LogMessage.REQUEST_MAP_API_LOG.format(date_time=datetime.now(),
                                                                  email=email))

            pending_time = current_pending_time.seconds - ride_time

            logger.info(f"pending_time: {pending_time}, current_pending_time: "
                        f"{current_pending_time.seconds}, ride_time: {ride_time}")

            logger.info(f"uber_time + error_margin: "
                        f"{settings.UBER_TIME + settings.ERROR_MARGIN_TIME}")

            if pending_time <= settings.UBER_TIME + settings.ERROR_MARGIN_TIME:
                ScheduleTrip.book_uber(response, email, source)
            else:
                ScheduleTrip.update_trip_details(ride_time, traffic_time,
                                                 pending_time, trip_id)

        return response

import logging
from datetime import datetime

import googlemaps
from django.conf import settings

from utils.utils import convert_str_to_lat_long

logger = logging.getLogger('custom-module')


class GoogleMaps:
    client = googlemaps.Client(key=settings.GOOGLE_MAP_API_KEY)

    @classmethod
    def get_static_ride_time(cls, source, destination):
        source = convert_str_to_lat_long(source)
        destination = convert_str_to_lat_long(destination)

        for i in range(3):
            try:
                distance_matrix = cls.client.distance_matrix(source, destination)
                break
            except Exception as ex:
                logger.info(f"Retrying Google Maps api... {i}")
                if i == 2:
                    raise ex

        distance_matrix = cls.client.distance_matrix(source, destination)
        ride_time = distance_matrix.get('rows')[0].get('elements')[0].get('duration').get('value')
        return ride_time

    @classmethod
    def get_dynamic_ride_time(cls, source, destination):
        source = convert_str_to_lat_long(source)
        destination = convert_str_to_lat_long(destination)

        for i in range(3):
            try:
                distance_matrix = cls.client.distance_matrix(source, destination,
                                                             departure_time=datetime.now())
                break
            except Exception as ex:
                logger.info(f"Retrying Google Maps api... {i}")
                if i == 2:
                    raise ex

        distance_matrix = cls.client.distance_matrix(source, destination, departure_time=datetime.now())
        ride_time = distance_matrix.get('rows')[0].get('elements')[0].get('duration_in_traffic').get('value')
        return ride_time


if __name__ == '__main__':
    g = GoogleMaps()

    source_temp = (41.43206, -81.38992)
    destination_temp = (42.8863855, -78.8781627)
    # g.get_static_ride_time(source_temp, destination_temp)
    # g.get_dynamic_ride_time(source)

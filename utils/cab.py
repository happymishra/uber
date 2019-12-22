import logging

import requests
from django.conf import settings

logger = logging.getLogger('custom-module')


class Cab:
    def __init__(self):
        pass

    @staticmethod
    def get_uber(source):
        params = {'start_longitude': source[1],
                  'start_latitude': source[0]}

        for i in range(3):
            try:
                r = requests.get(settings.UBER_API, params)
                break
            except Exception as ex:
                logger.info(f"Retrying uber api... {i}")
                if i == 2:
                    raise ex

        nearest_cabs = r.json().get('times')
        nearest_cab_estimate_time = nearest_cabs[0].get('estimate')

        return int(nearest_cab_estimate_time)


if __name__ == '__main__':
    source_param = (41.43206, -81.38992)
    Cab.get_nearest_uber(source_param)

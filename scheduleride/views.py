import logging
import traceback

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from scheduleride.schedule_trip import ScheduleTrip
from scheduleride.serializer import TripSerializer

logger = logging.getLogger('custom-module')


class TripView(APIView):
    def __int__(self):
        pass

    def get(self, request):
        try:
            resp = ScheduleTrip.get_all_ride_details()
            data = {'data': resp}
            return JsonResponse(data, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(traceback.format_exc())
            return Response({'data': f"An error occurred {str(ex)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            trip_serializer = TripSerializer(data=request.data)

            if trip_serializer.is_valid():
                trip_serializer.save()
                return Response(trip_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            logger.error(traceback.format_exc())
            return Response(trip_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HTMLView(APIView):
    def __int__(self):
        pass

    def get(self, request):
        return render(request, 'scheduleride/trip_request.html')

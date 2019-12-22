from rest_framework import serializers

from .models import Trips


class TripSerializer(serializers.ModelSerializer):
    ride_time = serializers.ReadOnlyField()

    class Meta:
        model = Trips
        fields = ['source', 'destination', 'email', 'time_to_reach_dest', 'ride_time']

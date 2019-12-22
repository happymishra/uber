from django.db import models

from utils.googlemaps import GoogleMaps


class Trips(models.Model):
    class TripState(models.IntegerChoices):
        NEW = 1
        IN_PROGRESS = 2
        DONE = 3

    id = models.AutoField(primary_key=True)
    source = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    time_to_reach_dest = models.DateTimeField()
    email = models.EmailField(max_length=100)
    creation_time = models.DateTimeField(auto_now=True)
    ride_time = models.IntegerField()
    state = models.CharField(max_length=5, choices=TripState.choices, default=TripState.NEW)
    pending_time = models.IntegerField(default=0)
    frequency = models.SmallIntegerField(default=0)
    traffic_time = models.IntegerField()

    def save(self, *args, **kwargs):
        self.ride_time = GoogleMaps.get_static_ride_time(self.source, self.destination)
        self.traffic_time = self.ride_time
        self.time_to_reach_dest = self.time_to_reach_dest.replace(microsecond=0)
        super(Trips, self).save(*args, **kwargs)

    class Meta:
        db_table = "scheduled_trip"

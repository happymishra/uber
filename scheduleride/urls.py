from django.urls import path

from scheduleride import views

urlpatterns = [
    path('api/trip/', views.TripView.as_view()),
    path('', views.HTMLView.as_view())
]

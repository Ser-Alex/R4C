from django.urls import path, include

from .views import (
    api_robots,
)

app_name = "robots"


urlpatterns = [
    path('api/robots/',  api_robots, name='api_robots'),
]
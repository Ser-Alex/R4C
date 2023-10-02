from django.urls import path, include

from .views import (
    api_robots,
    robots_index_excel,
)

app_name = "robots"


urlpatterns = [
    path('api/robots/',  api_robots, name='api_robots'),
    path('robots/excel/download/',  robots_index_excel, name='robots_excel_download'),
]
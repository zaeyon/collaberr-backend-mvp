from django.urls import path
from core.api.creators.views import request_to_join_campaign


urlpatterns = [
    path('creator/join-campaign/', request_to_join_campaign),
]

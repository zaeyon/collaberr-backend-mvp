from django.urls import path
from .views import YoutubeChannelRegisterView


urlpatterns = [
    path("creator/register/youtube/", YoutubeChannelRegisterView.as_view()),
]

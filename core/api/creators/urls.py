from django.urls import path
from rest_framework.routers import SimpleRouter
from views import YoutubeChannelRegisterView

router = SimpleRouter()

urlpatterns = [
    path("creator/register/youtube/", YoutubeChannelRegisterView.as_view()),
]

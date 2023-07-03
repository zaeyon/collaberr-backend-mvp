from django.urls import path
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

urlpatterns = [
    path("creator/register/youtube/", CreatorYoutubeRegisterView.as_view()),
]


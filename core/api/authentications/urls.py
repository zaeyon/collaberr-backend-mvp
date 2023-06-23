from django.urls import path
from .views import CustomTokenRefreshView, YoutubeAuthView, YoutubeCallbackView, YoutubeRevokeView, DummyView

urlpatterns = [
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('youtube/auth/', YoutubeAuthView.as_view(), name='youtube_auth'),
    path('youtube/oauth2callback/', YoutubeCallbackView.as_view(), name='youtube_callback'),
    path('youtube/revoke/', YoutubeRevokeView.as_view(), name='youtube_revoke'),
    path('dummy_confirm/', DummyView.as_view(), name='dummy_view'),
]

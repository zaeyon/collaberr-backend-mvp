from django.urls import path
from .views import CustomTokenRefreshView

urlpatterns = [
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]

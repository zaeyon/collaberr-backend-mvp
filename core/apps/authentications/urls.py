from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import CustomTokenRefreshView

urlpatterns = [
    # path('refresh-token/', views.TokenRefreshView.as_view(), name='refresh-token'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]

from django.http import HttpResponse, HttpResponseBadRequest
from django.utils import timezone
from django.conf import settings
# drf imports
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
# drf_simplejwt imports
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
# collaberr imports
from .models import JWTToken
from core.general.authentication import CustomJWTAuthentication


class CustomTokenRefreshView(TokenRefreshView):
    """
    POST with empty body to refresh access token
    which will be stored in cookie
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        token_obj = JWTToken.objects.get(refresh_token=refresh_token)
        if not token_obj:
            return HttpResponseBadRequest("Invalid refresh token")

        # if someone tries to refresh token of another user
        if token_obj.account_id != request.user:
            return HttpResponseBadRequest("Invalid user for refresh token")

        token = RefreshToken(refresh_token)
        access_token = str(token.access_token)
        token_obj.access_token = access_token
        token_obj.access_expires_at = timezone.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        token_obj.save()
        response = HttpResponse(status=status.HTTP_200_OK)

        # SECURITY WARNING: Don't store access_token in cookie in production or Hash it
        response.set_cookie('access_token', access_token, httponly=True, secure=True, samesite='None')
        return response

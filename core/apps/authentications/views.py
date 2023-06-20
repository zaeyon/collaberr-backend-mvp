from .models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import HttpResponseBadRequest
from django.utils import timezone
from core.general.constants import ACCESS_TOKEN_LIFETIME


class CustomTokenRefreshView(TokenRefreshView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        token_obj = Token.objects.get(refresh_token=refresh_token)

        if not token_obj:
            return HttpResponseBadRequest("Invalid refresh token")

        if token_obj.account_id != request.user:
            return HttpResponseBadRequest("Invalid user for refresh token")

        token = RefreshToken(refresh_token)
        access_token = str(token.access_token)
        token_obj.access_token = access_token
        token_obj.access_expires_at = timezone.now() + ACCESS_TOKEN_LIFETIME
        token_obj.save()

        response = Response({'access_token': access_token})
        response.set_cookie('access_token', access_token, httponly=True)
        return response

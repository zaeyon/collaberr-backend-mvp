# collaberr improts
from .models import Token
from core.general.constants import ACCESS_TOKEN_LIFETIME
# drf imports
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# drf_simplejwt imports
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.authentication import JWTAuthentication
# django imports
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.views import View
# google imports
from google_auth_oauthlib.flow import Flow
import requests


CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly']
REDIRECT_URI = "http://localhost:8000/api/youtube/oauth2callback/"


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


class YoutubeAuthView(View):
    def get(self, request):
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI
        )
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )

        return redirect(authorization_url)


class YoutubeCallbackView(View):
    def get(self, request):
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI
        )
        authorization_response = request.build_absolute_uri()
        flow.fetch_token(authorization_response=authorization_response)

        credentials = flow.credentials
        request.session['credentials'] = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }

        return redirect('http://localhost:3000/')


class YoutubeRevokeView(View):
    def get(self, request):
        revoke_url = 'https://oauth2.googleapis.com/revoke'
        params = {'token': request.session['credentials']['token']}
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(revoke_url, params=params, headers=headers)

        if response.status_code == 200:
            return HttpResponse('Successfully disconnected')
        else:
            return HttpResponseBadRequest('Failed to disconnect Youtube account')

# collaberr improts
from .models import JWTToken
from .serializers import YoutubeCredentialsSerializer
from core.general.authentication import CustomJWTAuthentication
# drf imports
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
# drf_simplejwt imports
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
# django imports
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import redirect
from django.utils import timezone
from django.conf import settings
# google imports
from google_auth_oauthlib.flow import Flow
import requests
from urllib.parse import urlencode, parse_qs, urlparse


SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly']
REDIRECT_URI = "http://localhost:8000/api/youtube/oauth2callback/"


class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        token_obj = JWTToken.objects.get(refresh_token=refresh_token)

        if not token_obj:
            return HttpResponseBadRequest("Invalid refresh token")

        if token_obj.account_id != request.user:
            return HttpResponseBadRequest("Invalid user for refresh token")

        token = RefreshToken(refresh_token)
        access_token = str(token.access_token)
        token_obj.access_token = access_token
        token_obj.access_expires_at = timezone.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        token_obj.save()

        response = Response({'access_token': access_token})
        # SECURITY WARNING: Don't store access_token in cookie in production
        response.set_cookie('access_token', access_token, httponly=True)
        return response


class YoutubeAuthView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def get(self, request):
        if request.user.is_authenticated:
            flow = Flow.from_client_secrets_file(
                settings.YOUTUBE_SECRETS_FILE,
                scopes=SCOPES,
                redirect_uri=REDIRECT_URI
            )
            authorization_url, state = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true'
            )
            return JsonResponse({'authorization_url': authorization_url})
        else:
            return HttpResponseForbidden('Access denied')


class YoutubeCallbackView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def get(self, request):
        flow = Flow.from_client_secrets_file(
            settings.YOUTUBE_SECRETS_FILE,
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI,
        )
        authorization_response = request.build_absolute_uri()
        flow.fetch_token(authorization_response=authorization_response)

        credentials = flow.credentials
        redirect_url = 'http://localhost:8000/api/youtube/confirm/?' + urlencode({
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scope': credentials.scopes[0],
        })

        response = HttpResponseRedirect(redirect_url)
        return response


class YoutubeConfirmView(APIView):
    permission_classes = [IsAuthenticated]
    # SECURITY WARNING, Don't pass in through URL and need authentication!
    authentication_classes = [CustomJWTAuthentication]

    def get(self, request):
        url = request.build_absolute_uri()
        url_components = urlparse(url)
        params = parse_qs(url_components.query)
        params = {key: value[0] for key, value in params.items()}

        serializer = YoutubeCredentialsSerializer(data=params, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return redirect('http://localhost:3000/youtubeConfirm/')
        return HttpResponseBadRequest('Invalid parameters')


class YoutubeRevokeView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def get(self, request):
        revoke_url = 'https://oauth2.googleapis.com/revoke'
        params = {'token': request.session['credentials']['token']}
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(revoke_url, params=params, headers=headers)

        if response.status_code == 200:
            return HttpResponse('Successfully disconnected')
        else:
            return HttpResponseBadRequest('Failed to disconnect Youtube account')

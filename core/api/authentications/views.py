# collaberr improts
from .models import JWTToken
from core.general.constants import ACCESS_TOKEN_LIFETIME
from .serializers import YoutubeCredentialsSerializer
# drf imports
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
# drf_simplejwt imports
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.authentication import JWTAuthentication
# django imports
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import redirect
from django.utils import timezone
# google imports
from google_auth_oauthlib.flow import Flow
import requests
from urllib.parse import urlencode, parse_qs


CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly']
REDIRECT_URI = "http://localhost:8000/api/youtube/oauth2callback/"


class CustomTokenRefreshView(TokenRefreshView):
    authentication_classes = [JWTAuthentication]
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
        token_obj.access_expires_at = timezone.now() + ACCESS_TOKEN_LIFETIME
        token_obj.save()

        response = Response({'access_token': access_token})
        # SECURITY WARNING: Don't store access_token in cookie in production
        response.set_cookie('access_token', access_token, httponly=True)
        return response


class YoutubeAuthView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_authenticated:
            flow = Flow.from_client_secrets_file(
                CLIENT_SECRETS_FILE,
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
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI,
        )
        authorization_response = request.build_absolute_uri()
        flow.fetch_token(authorization_response=authorization_response)

        credentials = flow.credentials
        request.session['youtube_credentials'] = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scope': credentials.scopes[0]
        }
        # access_token = request.headers.get('Authorization', '').replace('Bearer ', '')

        redirect_url = 'http://localhost:3000/campaigns'
        response = HttpResponseRedirect(redirect_url)
        # response['Authorization'] = f'Bearer {access_token}'

        return response


class YoutubeRevokeView(APIView):
    def get(self, request):
        revoke_url = 'https://oauth2.googleapis.com/revoke'
        params = {'token': request.session['credentials']['token']}
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(revoke_url, params=params, headers=headers)

        if response.status_code == 200:
            return HttpResponse('Successfully disconnected')
        else:
            return HttpResponseBadRequest('Failed to disconnect Youtube account')


class DummyView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        youtube_credentials = request.data.get('youtube_credentials')
        if request.user.is_authenticated and youtube_credentials:
            serializer = YoutubeCredentialsSerializer(account_id=request.user, data=youtube_credentials)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response('Successfully connected Youtube account')
            return Response(serializer.errors, status=400)
        return Response('Invalid or missing credentials', status=400)

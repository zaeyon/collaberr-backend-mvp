from django.utils import timezone
from django.contrib.auth.models import update_last_login
from django.http import HttpResponse
from django.conf import settings
from django.middleware import csrf
from django.contrib.auth import authenticate, login

# DRF imports
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics

# JWT imports
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.authentication import AUTH_HEADER_TYPES
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# collaberr imports
from .serializers import AccountCreateSerializer, AccountUpdateSerializer, AccountViewSerializer
from .models import Account
from core.general.permissions import IsAccountOwnerOrAdmin
from core.api.authentications.models import JWTToken

import logging

logger = logging.getLogger(__name__)


class AccountViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    serializer_class = AccountCreateSerializer
    queryset = Account.objects.none()

    def retrieve(self, request, *args, **kwargs):
        account = self.get_object()
        serializer = self.get_serializer(account)
        logger.info(f"Account retrieved: {serializer.data}")
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(f"Account created: {serializer.data}")
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Handle account update
    def partial_update(self, request, *args, **kwargs):
        account = self.get_object()
        serializer = self.get_serializer(account, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(f"Account updated: {serializer.data}")
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Account.objects.filter(id=self.request.user.id)
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action in ['update', 'delete', 'partial_update']:
            return AccountUpdateSerializer
        elif self.action in ['retrieve']:
            return AccountViewSerializer
        return AccountCreateSerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'delete', 'partial_update']:
            return [IsAccountOwnerOrAdmin()]
        return [AllowAny()]


# SECURITY WARNING: TO DO, Hash tokens
class CustomLoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = TokenObtainPairSerializer
    www_authenticate_realm = "api"

    def get_authenticate_header(self, request):
        return '{} realm="{}"'.format(
            AUTH_HEADER_TYPES[0],
            self.www_authenticate_realm,
        )

    def get(self, request, *args, **kwargs):
        return HttpResponse(status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        response = HttpResponse(status=status.HTTP_200_OK)
        user = Account.objects.get(email=request.data['email'])
        serializer.validated_data['account_id'] = user.id
        tokens = serializer.validated_data
        # TO DO: Make this into Model Manager
        authenticated_user = authenticate(request, email=request.data['email'], password=request.data['password'])
        if authenticated_user:
            login(request, authenticated_user)

            update_last_login(None, authenticated_user)

            refresh_token = tokens['refresh']
            access_token = tokens['access']
            # TO DO: Handle this with Model Manager
            try:
                token = JWTToken.objects.get(account_id=user)
                if token:
                    token.refresh_token = refresh_token
                    token.access_token = access_token
                    token.refresh_expires_at = timezone.now() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
                    token.access_expires_at = timezone.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
                    token.save()
            except JWTToken.DoesNotExist:
                JWTToken.objects.create(
                    account_id=user,
                    refresh_token=refresh_token,
                    access_token=access_token,
                    refresh_expires_at=timezone.now() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                    access_expires_at=timezone.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
                )
            csrf.get_token(request)
            # SECURITY WARNING: Encryption needed
            response.set_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'], access_token, httponly=True, secure=True, samesite='None')
            response.set_cookie('refresh_token', refresh_token, httponly=True, secure=True, samesite='None')
            response.set_cookie('account_id', user.id, httponly=False)
            logger.info(f"Account logged in: {user.email}")
        return response


# TO DO: Is there an exsiting django view?
class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        response = HttpResponse(status=status.HTTP_200_OK)
        response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'])
        response.delete_cookie('account_id')
        response.delete_cookie('sessionid')
        response.delete_cookie('refresh_token')
        logger.info(f"Account logged out: {request.user.email}")
        return response

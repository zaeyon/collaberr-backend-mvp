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
from rest_framework.permissions import AllowAny
from rest_framework import generics

# JWT imports
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.authentication import AUTH_HEADER_TYPES
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# collaberr imports
from .serializers import AccountCreateSerializer, AccountUpdateSerializer
from .models import Account
from core.general.permissions import IsAccountOwnerOrAdmin
from core.api.authentications.models import JWTToken


class AccountViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    serializer_class = AccountCreateSerializer
    queryset = Account.objects.none()

    def retrieve(self, request, *args, **kwargs):
        account = self.get_object()
        serializer = self.get_serializer(account)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Handle account update
    def partial_update(self, request, *args, **kwargs):
        account = self.get_object()
        serializer = self.get_serializer(account, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Account.objects.filter(id=self.request.user.id)
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action in ['retrieve', 'update', 'delete', 'partial_update']:
            return AccountUpdateSerializer
        return AccountCreateSerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'delete', 'partial_update']:
            return [IsAccountOwnerOrAdmin()]
        return [AllowAny()]


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

        authenticated_user = authenticate(request, email=request.data['email'], password=request.data['password'])
        if authenticated_user:
            login(request, authenticated_user)

            update_last_login(None, authenticated_user)

            refresh_token = tokens['refresh']
            access_token = tokens['access']
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
            response.set_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'], access_token, httponly=True, secure=True, samesite='None')
            response.set_cookie('account_id', user.id, httponly=False)
        return response

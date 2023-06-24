from django.utils import timezone
from django.contrib.auth.models import update_last_login
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

# DRF imports
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

# JWT imports
from rest_framework_simplejwt.views import TokenObtainPairView

# collaberr imports
from .serializers import AccountCreateSerializer, AccountUpdateSerializer
from .models import Account
from core.general.permissions import IsAccountOwnerOrAdmin
from core.general.constants import REFRESH_TOKEN_LIFETIME, ACCESS_TOKEN_LIFETIME
from core.api.authentications.models import JWTToken


class AccountViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    serializer_class = AccountCreateSerializer
    queryset = Account.objects.none()

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


class CustomLoginView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return HttpResponse(status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            user = Account.objects.get(email=request.data['email'])
            update_last_login(None, user)
            response.data['account_id'] = user.id
            refresh_token = response.data['refresh']
            access_token = response.data['access']
            try:
                token = JWTToken.objects.get(account_id=user)
                if token:
                    token.refresh_token = refresh_token
                    token.access_token = access_token
                    token.refresh_expires_at = timezone.now() + REFRESH_TOKEN_LIFETIME
                    token.access_expires_at = timezone.now() + ACCESS_TOKEN_LIFETIME
                    token.save()
            except JWTToken.DoesNotExist:
                JWTToken.objects.create(
                    account_id=user,
                    refresh_token=refresh_token,
                    access_token=access_token,
                    refresh_expires_at=timezone.now() + REFRESH_TOKEN_LIFETIME,
                    access_expires_at=timezone.now() + ACCESS_TOKEN_LIFETIME
                )

        return response

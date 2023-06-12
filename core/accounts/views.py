from django.shortcuts import render
from django.contrib.auth import authenticate

# DRF imports
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.authtoken.models import Token

# collaberr imports
from .serializers import AccountCreateSerializer, AccountUpdateSerializer
from .models import Account
from core.general.permissions import IsAccountOwnerOrAdmin


class AccountViewSet(ModelViewSet):

    # TODO MEDIUM: could have to restrict permissions
    permission_classes = [AllowAny]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    serializer_class = AccountCreateSerializer
    queryset = Account.objects.none()

    # Handle account creation
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


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            else:
                return Response({'error': 'Invalid email/password'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Missing email/password'}, status=status.HTTP_400_BAD_REQUEST)

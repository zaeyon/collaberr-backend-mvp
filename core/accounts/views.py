from django.shortcuts import render

# DRF imports
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission

# collaberr imports
from .serializers import AccountCreateSerializer, AccountUpdateSerializer
from .models import Account
from core.general.authentications import IsAccountOwnerOrAdmin


class AccountViewSet(ModelViewSet):

    # TODO MEDIUM: could have to restrict permissions
    permission_classes = [AllowAny]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    serializer_class = AccountCreateSerializer

    # Handle account creation
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED,
                    )
        return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
                )
    
    # Handle account update
    def partial_update(self, request, *args, **kwargs):
        account = self.get_object()
        serializer = self.get_serializer(account, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                    serializer.data,
                    status=status.HTTP_200_OK,
                    )
        return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
                )
   
    def get_queryset(self):
        return Account.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return AccountCreateSerializer
        elif self.action in ['retrieve', 'update', 'delete', 'partial_update']:
            return AccountUpdateSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        elif self.action in ['retrieve', 'update', 'delete', 'partial_update']:
            return [IsAccountOwnerOrAdmin()]
        return super().get_permissions()

from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import AccountSerializer
from .models import Account

import random
import re


class AccountViewSet(ModelViewSet):
    serializer_class = AccountSerializer
    # TODO MEDIUM: could have to restrict permissions
    authentication_classes = []
    permission_classes = [AllowAny]

    # def get_queryset(self):
        # return Account.objects.all()

    def create(self, request, *args, **kwargs):
        account_id = self.generate_account_id()
        request.data['account_id'] = account_id
        serializer = AccountSerializer(data=request.data)
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
    
    def generate_account_id(self):
        pattern = re.compile(r'[0-9a-f]{16}')
        while True:
            account_id = ''.join(random.choices('0123456789abcdef', k=16))
            if re.match(pattern, account_id):
                return account_id

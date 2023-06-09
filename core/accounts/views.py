from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import AccountSerializer
from .models import Account

class AccountViewSet(ModelViewSet):
    serializer_class = AccountSerializer

    def get_queryset(self):
        return Account.objects.all()

    def post(self, request):
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

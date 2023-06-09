from rest_framework import serializers
from .models import Account

import random
import re

class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ['account_id', 'username', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        account_id = validated_data.pop('account_id')
        user = Account.objects.create_user(
                username=validated_data['username'],
                account_id = account_id,
                password=password,
                )
        return user

from rest_framework import serializers
from django.db import IntegrityError
from .models import Account
import random
import re

class AccountCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ['username', 'password', 'email', 'role']

    def create(self, validated_data):
        password = validated_data.pop('password')

        # validate that the account_id is unique in the database
        while True:
            account_id = self.generate_account_id()
            try:
                user = Account.objects.create_user(
                        username=validated_data['username'],
                        id = account_id,
                        password=password,
                        role=validated_data['role'],
                        email = validated_data['email'],
                        )
                return user
            except IntegrityError:
                continue

    def generate_account_id(self):
        pattern = re.compile(r'[0-9a-f]{16}')
        return ''.join(random.choices('0123456789abcdef', k=16))

# Fields = fields that I can update with "edit profile" link
class AccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['username', 'email', 'first_name', 'last_name']
        

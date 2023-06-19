from rest_framework import serializers
from django.db import IntegrityError
from .models import Account
import random


class AccountCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ['username', 'password', 'password_confirm', 'email', 'role']

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        # validate that the account_id is unique in the database
        while True:
            account_id = self.generate_account_id()
            try:
                user = Account.objects.create_user(**validated_data, id=account_id, password=password)
                return user
            except IntegrityError:
                continue

    def generate_account_id(self):
        return ''.join(random.choices('0123456789abcdef', k=16))


# Fields that I can update with "edit profile" link
class AccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['username', 'email', 'first_name', 'last_name']

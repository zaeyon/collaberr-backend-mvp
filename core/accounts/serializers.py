from rest_framework import serializers

from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['account_id', 'username', 'balance']
        read_only_fields = ['account_id', 'balance']

    def create(self, validated_data):
        user = Account.objects.create_user(
                username=validated_data['username'],
                password=validated_data['password'],
                )
        return user

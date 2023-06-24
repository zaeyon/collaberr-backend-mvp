from rest_framework import serializers
from .models import YoutubeCredential, JWTToken
from core.api.accounts.models import Account


class YoutubeCredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = YoutubeCredential
        fields = ['token', 'refresh_token', 'token_uri', 'client_id', 'client_secret', 'scope']

    def create(self, validated_data):
        # access_token = validated_data.pop('access_token')
        user_id = JWTToken.objects.get(access_token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg3NjA2ODQxLCJpYXQiOjE2ODc1ODUyNDEsImp0aSI6ImY0NWFiNWE0YWQwMTQ4ZWJiYzg0ZTRjOGQwNDJjY2YwIiwidXNlcl9pZCI6ImIzMDdhOWUxMjM1ZWJmYzIifQ.eKIXagQsyIL78KoFbvNFDDP4-1eZp2btM2AoxzFCFZo').account_id_id
        user = Account.objects.get(id=user_id)
        validated_data['account_id'] = user
        return YoutubeCredential.objects.create(**validated_data)

    def validate(self, data):
        data = super().validate(data)
        return data

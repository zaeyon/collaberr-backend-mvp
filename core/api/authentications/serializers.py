from rest_framework import serializers
from .models import YoutubeCredential


class YoutubeCredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = YoutubeCredential
        fields = ['token', 'refresh_token', 'token_uri', 'client_id', 'client_secret', 'scope']

    def create(self, validated_data):
        request = self.context.get('request')
        context = super().create({**validated_data, 'account_id': request.user})
        return context

    def validate(self, data):
        data = super().validate(data)
        return data

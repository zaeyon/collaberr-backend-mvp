from rest_framework import serializers
from core.api.youtube_analytics.models import YoutubeCredential
from core.api.accounts.models import Account
from core.api.creators.models import Creator


class YoutubeCredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = YoutubeCredential
        fields = ['token', 'refresh_token', 'token_uri', 'client_id', 'client_secret', 'scope']

    def create(self, validated_data):
        user_id = self.context['request'].COOKIES.get('account_id')
        user = Account.objects.get(id=user_id)
        validated_data['account_id'] = user
        creator_id = Creator.objects.get(account_id=user)
        validated_data['creator_id'] = creator_id
        return YoutubeCredential.objects.create(**validated_data)

    def validate(self, data):
        data = super().validate(data)
        return data

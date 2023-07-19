from rest_framework import serializers
from .models import Creator, ChannelBasic
from core.api.accounts.models import Account


class CreatorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creator
        fields = '__all__'


class ChannelBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelBasic
        fields = '__all__'

    def create(self, validated_data):
        user_id = self.context['request'].COOKIES.get('account_id')
        user = Account.objects.get(id=user_id)
        validated_data['account_id'] = user
        creator_id = Creator.objects.get(account_id=user)
        validated_data['creator_id'] = creator_id
        return ChannelBasic.objects.create(**validated_data)

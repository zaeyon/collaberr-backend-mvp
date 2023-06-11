from rest_framework import serializers
from .models import Campaign


class CampaignReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = '__all__'

class CampaignCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = '__all__'
        read_only_fields = ['owner', 'username']

    def create(self, validated_data):
        request = self.context.get('request')
        campaign = super().create({
                **validated_data,
                'owner': request.user,
                'username': request.user.username,
                })
        return campaign

    def validate(self, data):
        data = super().validate(data)
        request = self.context.get('request')
        return data

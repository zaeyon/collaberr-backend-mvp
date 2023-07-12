from rest_framework import serializers
from .models import Campaign

# campaign_display_fields = ['brand_name', 'title', 'thumbnail', 'category',
#                            'platform', 'start_date', 'end_date', 'description',
#                            'recruit_start_date', 'recruit_end_date',
#                            'mission_type', 'reward', 'additional_files',
#                            'created_at', 'modified_at', 'id']


class CampaignReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = '__all__'


class CampaignCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = '__all__'
        # These fields are populated in models.py or create method
        read_only_fields = ['owner', 'created_at', 'modified_at', 'id']

    def create(self, validated_data):
        request = self.context.get('request')
        campaign = super().create({**validated_data, 'owner': request.user})
        return campaign

    def validate(self, data):
        data = super().validate(data)
        return data

# Campaign Edit field which is only editable by owner


from rest_framework import serializers
from .models import Creator


class CreatorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creator
        fields = '__all__'

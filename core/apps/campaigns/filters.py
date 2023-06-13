import django_filters

from .models import Campaign

class CampaignFilter(django_filters.FilterSet):
    owner = django_filters.CharFilter(field_name='owner', lookup_expr='exact')
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    description = django_filters.CharFilter(field_name='description', lookup_expr='icontains')

    class Meta:
        model = Campaign
        fields = ['title', 'description', 'owner']

from rest_framework.routers import SimpleRouter
from django.urls import path

from core.api.campaigns.views import (
                                    CampaignViewSet,
                                    CampaignReadOnlyViewSet,
                                    ChangeCreatorStateView,
                                    CampaignCreatorsListView
                                )
router = SimpleRouter()

# api/campaigns
router.register('campaigns', CampaignViewSet, basename='campaigns')

urlpatterns = [
    path('campaigns/all/', CampaignReadOnlyViewSet.as_view({'get': 'list'}), name='all-campaigns'),
    path('campaigns/<int:campaign_id>/creator/', ChangeCreatorStateView.as_view(), name='change-creator-state'),
    path('campaigns/<int:campaign_id>/creator/all/', CampaignCreatorsListView.as_view(), name='campaign-creators'),
] + router.urls

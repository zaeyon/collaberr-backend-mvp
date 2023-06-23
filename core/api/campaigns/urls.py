from rest_framework.routers import SimpleRouter
from django.urls import path

from .views import CampaignViewSet, CampaignReadOnlyViewSet

router = SimpleRouter()

# api/campaigns
router.register('campaigns', CampaignViewSet, basename='campaigns')

urlpatterns = [
    # api/login
    path('campaigns/all/', CampaignReadOnlyViewSet.as_view({'get': 'list'}), name='all-campaigns'),
] + router.urls

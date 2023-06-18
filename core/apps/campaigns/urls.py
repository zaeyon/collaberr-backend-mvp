from rest_framework.routers import SimpleRouter

from .views import CampaignViewSet

router = SimpleRouter()

# api/campaigns
router.register('campaigns', CampaignViewSet, basename='campaigns')

urlpatterns = router.urls

from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import CampaignViewSet

router = SimpleRouter(trailing_slash=False)
router.register('campaigns', CampaignViewSet, basename='campaigns')

urlpatterns = router.urls

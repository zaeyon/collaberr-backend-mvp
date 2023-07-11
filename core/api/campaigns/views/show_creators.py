from django.http import HttpResponseBadRequest
from rest_framework.generics import ListAPIView

from core.general.permissions import IsBusiness
from core.api.creators.models import Creator
from core.api.creators.serializers import CreatorModelSerializer

import logging
logger = logging.getLogger(__name__)


class CampaignCreatorsListView(ListAPIView):
    """
    List all creators.
    """
    queryset = Creator.objects.all()
    permission_classes = [IsBusiness]
    serializer_class = CreatorModelSerializer

    def get(self, request, campaign_id):
        campaign = self.get_queryset().filter(campaigns_requested__id=campaign_id)
        if campaign:
            return self.list(self.request)
        else:
            return HttpResponseBadRequest('Campaign id is not provided')

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView

from core.api.campaigns.models import Campaign
from core.api.creators.models import Creator
from core.general.permissions import IsCampaignOwner

import logging
logger = logging.getLogger(__name__)


class ChangeCreatorStateView(UpdateAPIView):
    permission_classes = [IsCampaignOwner]
    queryset = Campaign.objects.all()

    def update(self, request, campaign_id):
        campaign = self.get_object(campaign_id)
        creator = Creator.objects.get(id=request.data['creator_id'])
        state = request.query_params.get('state')
        if campaign.is_active and campaign.is_recruiting:
            if state == 'approve':
                campaign.add_approved_creator(creator)
                return Response(status=status.HTTP_200_OK, data={'message': 'Successfully approved'})
            elif state == 'decline':
                campaign.add_declined_creator(creator)
                return Response(status=status.HTTP_200_OK, data={'message': 'Successfully declined'})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Campaign is not active'})

    def get_object(self, campaign_id):
        obj = get_object_or_404(self.get_queryset(), pk=campaign_id)
        self.check_object_permissions(self.request, obj)
        return obj

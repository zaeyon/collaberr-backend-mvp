from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from core.general.authentication import CustomJWTAuthentication


class YoutubeChannelRegisterView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def post(self, request, *args, **kwargs):
        channel_id = request.data['channel_id']
        return Response(status=status.HTTP_200_OK)

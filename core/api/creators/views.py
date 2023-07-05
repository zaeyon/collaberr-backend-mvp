from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Call this API to register YouTube Channel that has been authorized
class YoutubeChannelRegisterView(APIView):

    def post(self, request, *args, **kwargs):
        channel_id = request.data['channel_id']
        return Response(status=status.HTTP_200_OK)


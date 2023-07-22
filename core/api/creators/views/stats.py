from rest_framework.generics import ListAPIView
from rest_framework.response import Response


class CreatorStatsView(ListAPIView):
    """
    Get creator stats from Youtube API
    """
    def get(self, request):
        return Response('Hello World')

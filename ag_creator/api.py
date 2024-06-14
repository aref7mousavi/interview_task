from rest_framework.response import Response
from rest_framework.views import APIView

from ag_creator.methods import create_ag_queue


class AGAPIViewSet(APIView):

    def post(self, request, *args, **kwargs):
        """
        Starts to fill aggregation table
        """
        create_ag_queue.delay()
        return Response({'message': 'POST request received'}, status=200)
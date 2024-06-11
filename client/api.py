from rest_framework.response import Response
from rest_framework.views import APIView

from city.models import RawData
from client import CalStr


class APIViewSet(APIView):

    def validate_body(self, body):
        return not any(
            [not body.get("layer"), not body.get("elements"), not body.get("kpi")]
        )

    def site_handler(self, request):
        instances = RawData.objects.filter(site__in=request.data.get("elements"))
        res = {}
        for instance in instances:
            res[instance.site] = CalStr(request.data.get("kpi"), instance)
        return res

    def post(self, request, *args, **kwargs):
        if self.validate_body(request.data):
            return Response({'error': 'invalid params'}, status=400)
        if (layer := request.data.get("layer")) in ("site", "city", "province"):
            data = getattr(self, f"{layer}_handler")(request)
            return Response(data, 200)
        # Implement the logic for handling POST requests
        # Access request data using request.data
        # Process the data, perform validations, save to database, etc.
        return Response({'message': 'POST request received'}, status=200)
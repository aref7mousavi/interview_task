import re

from rest_framework.response import Response
from rest_framework.views import APIView

from city.models import AggregateModel
from client.methods import CalStr, CalCity, CalProvince


class ClientAPIViewSet(APIView):

    def validate_body(self, body):
        return any(
            [not body.get("layer"), not body.get("elements"), not body.get("kpi")]
        )

    def find_kpi(self, string):
        regex = r'kpi\_\d*'
        return re.findall(regex, string)

    def site_handler(self, request):
        kpi_list = self.find_kpi(request.data.get("kpi"))
        instances = AggregateModel.objects.select_related(
            "site",
            "site__city",
            "site__city__province",
        ).filter(
            site__name__in=request.data.get("elements")
        )
        return CalStr(request.data.get("kpi"), instances, kpi_list).start_calc()

    def city_handler(self, request):
        kpi_list = self.find_kpi(request.data.get("kpi"))
        if not kpi_list:
            return {}
        instances = AggregateModel.objects.select_related("city", "city__province").filter(
            city__name__in=request.data.get("elements"),
            kpi__in=kpi_list
        )
        return CalCity(request.data.get("kpi"), instances, kpi_list).start_calc()

    def province_handler(self, request):
        kpi_list = self.find_kpi(request.data.get("kpi"))
        if not kpi_list:
            return {}
        instances = AggregateModel.objects.select_related("province").filter(
            province__name__in=request.data.get("elements"),
            kpi__in=kpi_list
        )
        return CalProvince(request.data.get("kpi"), instances, kpi_list).start_calc()

    def post(self, request, *args, **kwargs):
        if self.validate_body(request.data):
            return Response({'error': 'invalid params'}, status=400)
        if (layer := request.data.get("layer")) in ("site", "city", "province"):
            data = getattr(self, f"{layer}_handler")(request)
            return Response(data, 200)
        return Response({'message': 'POST request received'}, status=200)

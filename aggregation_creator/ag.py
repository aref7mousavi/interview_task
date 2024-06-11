import django.db.models

from city.models import AggregateModel, RawData


def create_ag():
    from user_data.methods import AGGREGATIONS
    for key, value in AGGREGATIONS.items():
        if value in ("sum", "avg", "min", "max"):
            city_ag = []
            province_ag = []
            for city in RawData.objects.select_related("city").distinct("city").values_list("city", flat=True):
                result = RawData.objects.filter(city=city).aggregate(
                    summary=getattr(django.db.models, value.title())(key)
                )
                city_ag.append(AggregateModel(
                    city_id=city,
                    kpi=key,
                    value=result["summary"],
                    method=getattr(AggregateModel, value.upper())
                ))
            for province in RawData.objects.select_related(
                    "city__province"
            ).distinct("city__province").values_list("city__province", flat=True):
                result = RawData.objects.filter(city__province=province).aggregate(
                    summary=getattr(django.db.models, value.title())(key)
                )
                province_ag.append(AggregateModel(
                    province_id=province,
                    kpi=key,
                    value=result["summary"],
                    method=getattr(AggregateModel, value.upper())
                ))
            AggregateModel.objects.bulk_create(city_ag + province_ag)
    # TODO: request

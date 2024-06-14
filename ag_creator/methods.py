import django.db.models
from celery import shared_task

from city.models import AggregateModel, RawData


def create_ag():
    from user_data.methods import AGGREGATIONS
    for key, value in AGGREGATIONS.items():
        if value in ("sum", "avg", "min", "max"):
            city_ag = []
            province_ag = []
            for province in RawData.objects.select_related(
                    "site__city__province"
            ).distinct("site__city__province").values_list("site__city__province", flat=True):
                result = RawData.objects.filter(site__city__province=province).aggregate(
                    summary=getattr(django.db.models, value.title())(key)
                )
                province_ag.append(AggregateModel(
                    province_id=province,
                    kpi=key,
                    value=result["summary"],
                    method=getattr(AggregateModel, value.upper())
                ))
            for city in RawData.objects.select_related("site__city").distinct("site__city").values_list("site__city", flat=True):
                result = RawData.objects.filter(site__city=city).aggregate(
                    summary=getattr(django.db.models, value.title())(key)
                )
                city_ag.append(AggregateModel(
                    city_id=city,
                    kpi=key,
                    value=result["summary"],
                    method=getattr(AggregateModel, value.upper())
                ))
            for site in RawData.objects.select_related("site").distinct("site").values_list("site", flat=True):
                result = RawData.objects.filter(site=site).aggregate(
                    summary=getattr(django.db.models, value.title())(key)
                )
                city_ag.append(AggregateModel(
                    site_id=site,
                    kpi=key,
                    value=result["summary"],
                    method=getattr(AggregateModel, value.upper())
                ))
            AggregateModel.objects.bulk_create(city_ag + province_ag)
    # TODO: request


@shared_task
def create_ag_queue():
    create_ag()

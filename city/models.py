from django.db import models


class ABCName(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        abstract = True


class Province(ABCName):
    class Meta:
        verbose_name = "province"
        verbose_name_plural = "provinces"
        db_table = "province"


class City(ABCName):
    province = models.ForeignKey("Province", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "city"
        verbose_name_plural = "cities"
        db_table = "city"


class RawData(models.Model):
    city = models.ForeignKey("City", on_delete=models.CASCADE)
    day = models.DateTimeField()
    site = models.CharField(max_length=64)
    kpi_1 = models.FloatField()
    kpi_2 = models.FloatField()
    kpi_3 = models.FloatField()
    kpi_4 = models.FloatField()
    kpi_5 = models.FloatField()
    kpi_6 = models.FloatField()
    kpi_7 = models.FloatField()
    kpi_8 = models.FloatField()
    kpi_9 = models.FloatField()
    kpi_10 = models.FloatField()
    kpi_11 = models.FloatField()
    kpi_12 = models.FloatField()
    kpi_13 = models.FloatField()
    kpi_14 = models.FloatField()
    kpi_15 = models.FloatField()
    kpi_16 = models.FloatField()
    kpi_17 = models.FloatField()
    kpi_18 = models.FloatField()
    kpi_19 = models.FloatField()
    kpi_20 = models.FloatField()

    class Meta:
        verbose_name = "raw"
        verbose_name_plural = "raws"
        db_table = "raw"


class AggregateModel(models.Model):
    SUM = 1
    AVG = 2
    MIN = 3
    MAX = 4

    METHOD_CHOICES = (
        (SUM, "SUM"),
        (AVG, "AVG"),
        (MIN, "MIN"),
        (MAX, "MAX"),
    )

    city = models.ForeignKey("City", on_delete=models.CASCADE, null=True, blank=True)
    province = models.ForeignKey("Province", on_delete=models.CASCADE, null=True, blank=True)
    kpi = models.CharField(max_length=8)
    value = models.FloatField()
    method = models.PositiveSmallIntegerField(choices=METHOD_CHOICES)

    class Meta:
        # abstract = True
        verbose_name = "Aggregate Model"
        verbose_name_plural = "Aggregate Models"
        db_table = "aggregate_model"


# class SumAggregateModel(ABCAggregateModel):
#     class Meta:
#         verbose_name = "Sum Aggregate Model"
#         verbose_name_plural = "Sum Aggregate Models"
#         db_table = "sum_aggregate_model"
#
#
# class AvgAggregateModel(ABCAggregateModel):
#     class Meta:
#         verbose_name = "Avg Aggregate Model"
#         verbose_name_plural = "Avg Aggregate Models"
#         db_table = "avg_aggregate_model"
#
#
# class MinAggregateModel(ABCAggregateModel):
#     class Meta:
#         verbose_name = "Min Aggregate Model"
#         verbose_name_plural = "Min Aggregate Models"
#         db_table = "min_aggregate_model"


# class MaxAggregateModel(ABCAggregateModel):
#     class Meta:
#         verbose_name = "Max Aggregate Model"
#         verbose_name_plural = "Max Sum Aggregate Models"
#         db_table = "max_aggregate_model"

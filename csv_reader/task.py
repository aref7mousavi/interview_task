import os
import csv
from datetime import datetime

import requests
from django.conf import settings
from django.utils import timezone

from city.models import Province, City, RawData, Site


def create_raw(columns_name, chunk, city_dict):

    bulk_obj = []
    for obj in chunk:
        datetime_naive = datetime.strptime(obj[0], '%Y-%m-%d %H:%M:%S')
        aware_datetime = timezone.make_aware(datetime_naive, timezone.utc)
        obj[0] = aware_datetime

        create_data = dict(zip(columns_name, obj))
        site_key = (create_data.pop("site"), create_data.pop("city"), create_data.pop("province"))
        create_data["site"] = city_dict[site_key]
        bulk_obj.append(RawData(**create_data))
    RawData.objects.bulk_create(bulk_obj)


def create_province(names):
    Province.objects.bulk_create(
        [Province(name=name) for name in names]
    )


def create_city(names):
    bulk_obj = []
    province_dict = {province.name: province for province in Province.objects.all()}
    for name in names:
        city_name, province_name = name.split("__")
        bulk_obj.append(City(name=city_name, province=province_dict.get(province_name)))
    City.objects.bulk_create(bulk_obj)


def create_site(names):
    bulk_obj = []
    city_dict = {(city.name, city.province.name): city for city in City.objects.select_related("province").all()}
    for name in names:
        site_name, city_name, province_name = name.split("__")
        bulk_obj.append(Site(name=site_name, city=city_dict.get((city_name, province_name))))
    Site.objects.bulk_create(bulk_obj)


def csv_analyze():
    # cleaning database to start
    Province.objects.all().delete()

    root_path = os.path.dirname(__file__)
    file_path = os.path.join(root_path, '../user_data/data.csv')
    with open(file_path, 'r', encoding='utf-8') as file:
        data = csv.reader(file)
        columns_name = next(data)

        province_names = []
        province_index = columns_name.index("province")
        city_names = []
        city_index = columns_name.index("city")
        site_names = []
        site_index = columns_name.index("site")
        for row in data:
            province_names.append(row[province_index])
            city_names.append(f"{row[city_index]}__{row[province_index]}")
            site_names.append(f"{row[site_index]}__{row[city_index]}__{row[province_index]}")
        create_province(set(province_names))
        create_city(set(city_names))
        create_site(set(site_names))

    city_dict = {
        (
            site.name,
            site.city.name,
            site.city.province.name,
        ): site for site in Site.objects.select_related("city", "city__province").all()
    }
    with open(file_path, 'r', encoding='utf-8') as file:
        data = csv.reader(file)
        columns_name = next(data)

        while True:
            chunk = []
            try:
                for _ in range(500):  # chunk size
                    row = next(data)
                    chunk.append(row)
            except StopIteration:
                if chunk:  # Process the last chunk of data
                    create_raw(columns_name, chunk, city_dict)
                break

            create_raw(columns_name, chunk, city_dict)
    requests.post(url="http://" + settings.AGWEB_URL + ":8000/start/")

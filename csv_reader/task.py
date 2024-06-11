import os
import csv
from datetime import datetime

from city.models import Province, City, RawData


def create_raw(columns_name, chunk, city_dict):

    bulk_obj = []
    for obj in chunk:
        obj[0] = datetime.strptime(obj[0], '%Y-%m-%d %H:%M:%S')
        create_data = dict(zip(columns_name, obj))
        city_key = (create_data.pop("city"), create_data.pop("province"))
        create_data["city"] = city_dict[city_key]
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


def csv_analyze():
    root_path = os.path.dirname(__file__)
    file_path = os.path.join(root_path, '../user_data/data.csv')
    with open(file_path, 'r', encoding='utf-8') as file:
        data = csv.reader(file)
        columns_name = next(data)

        province_names = []
        province_index = columns_name.index("province")
        city_names = []
        city_index = columns_name.index("city")
        for row in data:
            province_names.append(row[province_index])
            city_names.append(f"{row[city_index]}__{row[province_index]}")
        create_province(set(province_names))
        create_city(set(city_names))

    city_dict = {(city.name, city.province.name): city for city in City.objects.select_related('province').all()}
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
    # TODO: request to aggregate

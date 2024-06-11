import os
import csv
from datetime import datetime
from time import sleep

from celery import Celery, Task, shared_task
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from flask import Flask

# Define your SQLAlchemy model
Base = declarative_base()


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


app = Flask(__name__)

app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://localhost",
        result_backend="redis://localhost",
        task_ignore_result=True,
    ),
)
celery = celery_init_app(app)


class Province(Base):
    __tablename__ = 'province'

    id = Column(Integer, primary_key=True)
    name = Column(String(64))


class City(Base):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    province_id = Column(Integer, ForeignKey('province.id'))
    province = relationship("Province", backref="cities")


class RawData(Base):
    __tablename__ = 'raw'

    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey('city.id'))
    city = relationship("City", backref="raw_data")
    day = Column(DateTime)
    site = Column(String(64))
    kpi_1 = Column(Float)
    kpi_2 = Column(Float)
    kpi_3 = Column(Float)
    kpi_4 = Column(Float)
    kpi_5 = Column(Float)
    kpi_6 = Column(Float)
    kpi_7 = Column(Float)
    kpi_8 = Column(Float)
    kpi_9 = Column(Float)
    kpi_10 = Column(Float)
    kpi_11 = Column(Float)
    kpi_12 = Column(Float)
    kpi_13 = Column(Float)
    kpi_14 = Column(Float)
    kpi_15 = Column(Float)
    kpi_16 = Column(Float)
    kpi_17 = Column(Float)
    kpi_18 = Column(Float)
    kpi_19 = Column(Float)
    kpi_20 = Column(Float)


# Connect to the database
engine = create_engine('postgresql://postgres:postgres@localhost:5432/city')
Session = sessionmaker(bind=engine)
session = Session()


def create_raw(columns_name, chunk):
    bulk_obj = []
    for obj in chunk:
        # Convert 'day' string to datetime object
        obj[0] = datetime.strptime(obj[0], '%Y-%m-%d %H:%M:%S')
        bulk_obj.append(RawData(**dict(zip(columns_name, obj))))
    session.bulk_save_objects(bulk_obj)
    session.commit()

def create_province(names):
    pass


@shared_task
def x():
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
            city_names.append(row[city_index])

        create_province(set(province_names))

        while True:
            chunk = []
            try:
                for _ in range(500):  # chunk size
                    row = next(data)
                    chunk.append(row)
            except StopIteration:
                if chunk:  # Process the last chunk of data
                    create_raw(columns_name, chunk)
                break

            create_raw(columns_name, chunk)


@app.route('/health')
def health_check():
    # Check if the task has finished successfully
    # Return appropriate response based on the task status
    return "Task finished successfully.", 200


@app.route('/csv')
def csv_serve():
    # Check if the task has finished successfully
    # Return appropriate response based on the task status
    x.delay()
    return "Done", 200


if __name__ == "__main__":
    # Your script logic here

    # Task completed successfully
    app.run(host='0.0.0.0', port=5000)

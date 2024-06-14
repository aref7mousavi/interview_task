to start services: docker compose up

you can change required aggregations and data.csv in user_data directory.

client api port is 8080
endpoint is /api/
request method is POST
e.g. http://localhost:8080/api/

this application contains:
postgresql
redis
celery
csv_reader
agweb (service to create aggregations)
client (web service)

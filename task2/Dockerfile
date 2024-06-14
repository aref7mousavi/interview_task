FROM python:3.9-slim

WORKDIR /app

COPY last_sport_news.py /app

RUN pip install --no-cache-dir  requests beautifulsoup4

# Run your Python script when the container launches
CMD ["python", "last_sport_news.py"]

FROM python:3.10.13

WORKDIR /mensa_scraper
COPY . /mensa_scraper

RUN apt-get update && \
    apt-get dist-upgrade -y && \
    apt-get install --no-install-recommends -y ca-certificates && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

HEALTHCHECK NONE

RUN chmod +x ./decode_service_key.sh

CMD ["sh", "-c", "./decode_service_key.sh && python main.py"]

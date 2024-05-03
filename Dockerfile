FROM python:3.10.13

WORKDIR /mensa_scraper
COPY . /mensa_scraper

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
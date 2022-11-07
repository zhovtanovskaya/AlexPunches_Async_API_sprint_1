FROM python:3.10-slim

WORKDIR /opt/app

COPY requirements.txt requirements.txt

RUN  pip install --no-cache-dir --upgrade pip \
     && apt-get -y update && apt-get -y install gcc libpq-dev python3-dev \
     && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "-b", "0.0.0.0:5000", "--workers", "4", "src.pywsgi:app"]
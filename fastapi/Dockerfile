FROM python:3.10-slim

WORKDIR /opt/app

COPY requirements.txt requirements.txt

RUN  pip install --no-cache-dir --upgrade pip \
     && apt-get -y update && apt-get -y install gcc libpq-dev python3-dev \
     && pip install --no-cache-dir -r requirements.txt

COPY . .

COPY ./wait-for-it.sh /opt/app/wait-for-it.sh

CMD ["gunicorn", "-b", "0.0.0.0:8000", "--workers", "4", "-k", "uvicorn.workers.UvicornWorker", "src.main:app"]
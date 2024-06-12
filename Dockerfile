FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_HOME /app

WORKDIR $APP_HOME

RUN apt-get update && \
    apt-get install -y postgis* binutils libproj-dev gdal-bin && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
COPY . .
RUN pip install -r requirements.txt

EXPOSE $PORT

CMD ["python", "manage.py", "runserver", "0.0.0.0:$PORT"]
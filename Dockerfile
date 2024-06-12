FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_HOME /app

WORKDIR $APP_HOME

RUN pip install --upgrade pip
COPY . .
RUN pip install -r requirements.txt

RUN apt-get install postgis* && \
    apt-get install binutils libproj-dev gdal-bin

EXPOSE $PORT

CMD ["sh", "-c", "python manage.py migrate && gunicorn", "--workers=2", "--threads=4", "--bind", "0.0.0.0:$PORT", "melpService.wsgi"]
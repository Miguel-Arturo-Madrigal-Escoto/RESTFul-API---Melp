FROM python:3.12.4-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_HOME /app

WORKDIR $APP_HOME

RUN pip install --upgrade pip
COPY . .
RUN pip install -r requirements.txt

RUN chmod +x ./app.sh
ENTRYPOINT [ "./app.sh" ]

EXPOSE $PORT

CMD ["gunicorn", "--workers=2", "--threads=4", "melpService.wsgi"]
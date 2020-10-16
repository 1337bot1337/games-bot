FROM python:3.8.2

RUN mkdir /src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY api/requirements.txt /src/api/

COPY ./docker/images/api/files/ /src/docker/
RUN apt update && apt install dos2unix
RUN dos2unix /src/docker/docker-entrypoint.sh

RUN chmod +x /src/docker/docker-entrypoint.sh \
    && pip install --upgrade pip \
    && pip install -r /src/api/requirements.txt

EXPOSE 8080

ENTRYPOINT ["/src/docker/docker-entrypoint.sh"]

COPY ./api /src/api/

WORKDIR /src/api

RUN python manage.py collectstatic --noinput

RUN mkdir -p /usr/local/public/media

CMD ["gunicorn", "-b", "0.0.0.0:8080", "core.config.wsgi:application", "-w", "5", "-t", "300"]

FROM nginx:1.19.0-alpine

RUN apk update \
    && apk add --no-progress \
            bash certbot openssl  \
    && rm /var/cache/apk/* \
    && echo "preparing certbot webroot" \
    && mkdir -p /var/lib/certbot \
    && echo "generating initial self-signed certificate" \
    && mkdir -p /etc/nginx/ssl/smarted/ \
    && openssl req -x509 -nodes -newkey rsa:4096 \
           -keyout /etc/nginx/ssl/smarted/privkey.pem \
           -out /etc/nginx/ssl/smarted/fullchain.pem \
           -subj "/C=/ST=/L=/O=/CN=smarted" \
    && ln -sf /etc/nginx/ssl/smarted /etc/nginx/ssl/latest

RUN rm /etc/nginx/conf.d/default.conf

COPY ./docker/images/nginx/files/default.conf /etc/nginx/conf.d
COPY ./docker/images/nginx/files/certbot.sh /etc/nginx/ssl/

RUN ["chmod", "+x", "/etc/nginx/ssl/certbot.sh"]

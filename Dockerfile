FROM python:3-alpine

RUN apk add --update && \
    pip install django && \
    pip install djangorestframework && \
    pip install markdown # Markdown support for the browsable API. \
    && rm -rf /var/cache/apk/*

RUN mkdir /django

WORKDIR /django

EXPOSE 80

COPY app/ /
RUN ls -alh

CMD ["python3", "/manage.py"]
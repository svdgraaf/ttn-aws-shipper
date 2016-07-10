FROM alpine:latest

RUN apk --no-cache add --update \
    python \
    python-dev \
    py-pip \
    build-base \
    libffi-dev \
    openssl-dev \
    ca-certificates \
  && pip install \
     virtualenv \
     supervisor \
     supervisor-stdout

WORKDIR /app

COPY supervisord.conf /etc/supervisord.conf
COPY . /app
RUN virtualenv /env \
    && /env/bin/pip install -r /app/requirements.txt

ENTRYPOINT ["supervisord", "--configuration", "/etc/supervisord.conf"]

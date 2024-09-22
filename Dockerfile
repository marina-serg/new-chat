
FROM python:3.12.0-alpine

RUN apk update && apk add --no-progress --no-cache \
    libpq-dev \
    gcc \
    musl-dev \
    openssl-dev \
    libffi-dev \
    python3-dev \
    supervisor \
    && rm -rf /var/lib/apt/lists/*



WORKDIR /app

COPY . /app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN pip install --upgrade pip --no-cache-dir --no-deps
RUN pip install -r requirements.txt --no-cache-dir



COPY supervisord.conf /etc/supervisord.conf

CMD ["supervisord", "-c", "/etc/supervisord.conf"]

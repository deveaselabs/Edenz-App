FROM python:3.12.5-alpine3.20

RUN pip install --upgrade pip

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY ./eden-app /app

WORKDIR /app

COPY ./entrypoint.sh /

ENTRYPOINT [ "sh", "/entrypoint.sh" ]
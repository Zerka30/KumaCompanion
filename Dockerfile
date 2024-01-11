FROM python:3.11-alpine

WORKDIR /app

COPY src /app/src
COPY utils /app/utils
COPY entrypoint.sh requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt \
    && chmod +x entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]
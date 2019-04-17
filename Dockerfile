# common-validations
# common validation services

ARG VERSION
ARG USER
FROM ${USER}/services-base:latest

RUN mkdir -p /app/service
COPY . /app/service
WORKDIR /app/service
RUN pip install -r requirements.txt
ENTRYPOINT ["/app/service/docker-entrypoint.sh"]

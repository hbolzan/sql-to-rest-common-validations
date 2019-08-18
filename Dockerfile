# common-validations
# common validation services

ARG VERSION
ARG USER
FROM ${USER}/services-base:latest

RUN mkdir -p /app/service
COPY . /app/service
WORKDIR /app/service
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
ENTRYPOINT ["/app/service/docker-entrypoint.sh"]

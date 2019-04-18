#!/bin/sh

until nc -z ${RABBIT_HOST} ${RABBIT_PORT}; do
    echo "$(date) - waiting for rabbitmq..."
    sleep 1
done

echo "AMQP_URI: amqp://${RABBIT_USER:-rabbitmq}:${RABBIT_PASSWORD:-rabbitmq}@${RABBIT_HOST:-nameko-rabbitmq}:${RABBIT_PORT:-5672}/" > config.yml
nameko run --config config.yml services

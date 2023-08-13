#!/bin/sh
( sleep 10 && \
rabbitmqctl add_user $RABBITMQ_USER $RABBITMQ_PASSWORD && \
rabbitmqctl set_user_tags $RABBITMQ_USER administrator && \
rabbitmqctl add_vhost psycho && \
rabbitmqctl set_permissions -p psycho $RABBITMQ_USER  ".*" ".*" ".*" ) & \
rabbitmq-server
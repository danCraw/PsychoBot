# Base for all images
FROM python:3.10.6 as python-base
# RUN addgroup -S psycho && adduser -S psycho -G psycho
COPY requirements.txt /tmp/requirements.txt
# ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
# RUN apk update && \
#     apk upgrade && \
#     apk add --update --no-cache \
#     bash \
#     wget \
#     postgresql-libs \
#     libjpeg \
#     zlib && \
#     apk add --update --no-cache -t .build-deps \
#     gcc \
#     openssl-dev \
#     jpeg-dev \
#     libffi-dev \
#     postgresql-dev \
#     zlib-dev \
#     build-base
RUN pip3 install -r /tmp/requirements.txt && rm -f /tmp/requirements.txt
# RUN apk del --purge .build-deps && \
#     rm -rf /var/cache/apk/*


# Build bot_consumer
FROM python-base as bot_consumer
ENV PYTHONPATH /app
ENV BOT_CONSUMER_LOG_FILE_PATH /var/log
ENV BOT_CONSUMER_LOG_FILE_NAME api_server
RUN ln -sf /proc/1/fd/1 /var/log/api_server.log
COPY core /app/core
COPY models /app/models
COPY db /app/db
COPY aiogramBot/consumer /app/aiogramBot/consumer
EXPOSE 10097
WORKDIR /app/aiogramBot/consumer
CMD ["python3", "-u", "main.py"]


# Build psychologists_bot
FROM python-base as psychologists_bot
ENV PYTHONPATH /app
ENV BOT_CONSUMER_LOG_FILE_PATH /var/log
ENV BOT_CONSUMER_LOG_FILE_NAME api_server
RUN ln -sf /proc/1/fd/1 /var/log/api_server.log
COPY core /app/core
COPY models /app/models
COPY db /app/db
COPY aiogramBot/psychologists /app/aiogramBot/psychologists
WORKDIR /app/aiogramBot/psychologists
CMD ["python3", "-u", "main.py"]


# Build psychologists_apis
FROM python-base as psychologists_apis
ENV PYTHONPATH /app
ENV BOT_CONSUMER_LOG_FILE_PATH /var/log
ENV BOT_CONSUMER_LOG_FILE_NAME api_server
RUN ln -sf /proc/1/fd/1 /var/log/api_server.log
COPY core /app/core
COPY models /app/models
COPY db /app/db
COPY apis /app//psychologists_apis
WORKDIR /app/psychologists_apis/app
CMD ["python3", "-u", "main.py"]


# # Build amin_panel
# FROM python-base as amin_panel_server
# ENV PYTHONPATH /app
# ENV BOT_CONSUMER_LOG_FILE_PATH /var/log
# ENV BOT_CONSUMER_LOG_FILE_NAME api_server
# RUN ln -sf /proc/1/fd/1 /var/log/api_server.log
# COPY psychoapp /app/psychoapp
# COPY app /app/app
# WORKDIR /app/app
# CMD ["python3", "-u", "manage.py runserver"]
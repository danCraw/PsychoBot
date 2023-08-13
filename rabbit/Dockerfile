FROM rabbitmq

# Define environment variables.
ENV RABBITMQ_USER 'psycho'
ENV RABBITMQ_PASSWORD 'password'
ENV RABBITMQ_VHOST 'password'

ADD init.sh /init.sh
RUN chmod +x /init.sh
EXPOSE 15672

# Define default command
CMD ["/init.sh"]
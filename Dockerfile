FROM python:3.7-alpine

RUN  pip install rungutan==1.1.2

VOLUME /root/.rungutan

VOLUME /project

WORKDIR /project

ENTRYPOINT ["/bin/sh", "-c"]

CMD ["rungutan", "help"]
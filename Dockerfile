FROM python:3.9-alpine

RUN  pip install rungutan==1.6.3

VOLUME /root/.rungutan

VOLUME /project

WORKDIR /project

CMD ["rungutan", "help"]

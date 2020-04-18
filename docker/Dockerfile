FROM docker.kiuber.me/base-alpine:1.0.0
RUN apk add --update nodejs npm
RUN mkdir -p /opt/node_npm_data && mkdir -p /opt/src
ADD package.json /opt/node_npm_data/package.json
RUN cd /opt/node_npm_data/ && npm install --loglevel verbose
WORKDIR /opt/src
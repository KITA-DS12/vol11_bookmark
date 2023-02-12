FROM node:18-alpine as build-stage

WORKDIR /client
COPY . .

RUN apk update && \
  npm install -g npm && \
  npm install -g @vue/cli

ADD ./client/package.json /client

RUN npm install

CMD ["npm", "run", "serve"]

FROM node:18-alpine

WORKDIR /client
COPY ./client .
ADD ./client/package.json /client

RUN npm install

CMD ["node_modules/.bin/vue-cli-servece", "serve" ]

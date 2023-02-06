FROM node:18-alpine as build-stage

WORKDIR /client
COPY . .

ADD ./client/package.json /client

RUN npm install

CMD ["npm", "run", "serve"]

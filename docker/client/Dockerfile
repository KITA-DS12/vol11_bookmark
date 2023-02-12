FROM node:18-bullseye as build-stage

WORKDIR /client
COPY . .

RUN apt-get update && apt-get upgrade -y
ADD ./client/package.json /client
RUN npm install

CMD ["npm", "run", "serve"]
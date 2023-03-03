FROM node:18-alpine

WORKDIR /client
COPY . .
ADD ./package.json /client

RUN npm install

CMD ["npm", "run", "serve" ]

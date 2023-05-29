FROM node:18-alpine

WORKDIR /client
COPY . .
ADD ./package.json /client

RUN npm install
RUN npm install @vue/cli

CMD ["npm", "run", "serve" ]

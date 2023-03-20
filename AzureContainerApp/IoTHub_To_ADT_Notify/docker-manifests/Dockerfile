FROM node:18.13-alpine3.17

RUN apk upgrade --no-cache

WORKDIR /app

COPY . .
RUN npm install

CMD [ "node", "index.js"]
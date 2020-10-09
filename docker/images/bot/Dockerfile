FROM node:12

RUN mkdir /src

COPY ./bot /src/bot/
RUN apt update

WORKDIR /src/bot

RUN npm install

RUN npm install nodemon --save-dev

EXPOSE 8081

# set param on 'start' for prod start bot
CMD ["npm", "run", "dev"]
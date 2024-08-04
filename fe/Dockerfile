FROM node:14

WORKDIR /app

COPY package*.json ./

RUN npm install
RUN npm install socket.io-client
RUN npm install xterm xterm-addon-fit
COPY . .

EXPOSE 7070

CMD ["npm", "run", "serve"]
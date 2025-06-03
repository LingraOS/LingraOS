FROM node:18
WORKDIR /app
COPY . .
RUN npm install http-proxy-middleware jsonwebtoken
RUN npm install
CMD ["npm", "run", "start"]
# develop stage
FROM node:12.16-alpine as develop-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
RUN npm install -g @quasar/cli@1.4.0
COPY . .

# build stage
FROM develop-stage as build-stage
RUN quasar build

# production stage
FROM nginx:1.15.7-alpine as production-stage
RUN mkdir /app
COPY --from=build-stage /app/dist/spa /etc/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

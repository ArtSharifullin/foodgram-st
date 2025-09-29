# build env
FROM node:21.7.1-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . ./
RUN npm run build
FROM nginx:alpine AS final
WORKDIR /usr/share/nginx/html
COPY --from=builder /app/build ./
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

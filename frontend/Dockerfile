FROM node:14-alpine AS builder

WORKDIR /app

COPY . .

RUN npm install

RUN npm run build -- --configuration production

FROM nginx:1.20.0-alpine

COPY --from=builder /app/dist/astronomy-search /usr/share/nginx/html

COPY --from=builder /app/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

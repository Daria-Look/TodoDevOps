# --- Frontend Dockerfile --- 

# Этап 1: Сборка проекта
FROM node:20-slim AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Этап 2: Запуск через Nginx
FROM nginx:stable-alpine
# Копируем конфиг
COPY nginx.conf /etc/nginx/conf.d/default.conf
# Копируем результат сборки из первого этапа
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 5173
CMD ["nginx", "-g", "daemon off;"]
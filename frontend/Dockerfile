# Etapa de construcción
FROM node:20-alpine AS build

WORKDIR /app

# Instalar dependencias
COPY package*.json ./
RUN npm install

# Copiar todo el proyecto y construir
COPY . .
RUN npm run build

# Etapa de producción
FROM nginx:alpine

# Copiar build al directorio de Nginx
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

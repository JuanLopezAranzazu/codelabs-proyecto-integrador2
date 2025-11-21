FROM node:20-alpine

WORKDIR /app

# Instalar dependencias
COPY package.json ./
RUN npm install --only=production

# Copiar código
COPY server.mjs ./server.mjs

EXPOSE 3000

CMD ["npm", "start"]


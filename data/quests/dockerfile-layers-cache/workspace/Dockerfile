FROM node:20-alpine
WORKDIR /app
# TODO: optimize cache by copying package.json first
COPY . .
RUN npm ci
CMD ["node", "server.js"]

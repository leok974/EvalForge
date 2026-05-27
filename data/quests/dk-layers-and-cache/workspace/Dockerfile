FROM node:20-slim
WORKDIR /app
# BUG: Wrong order! Copying all files before package.json busts the cache on every code change.
COPY . .
COPY package.json .
RUN npm install
CMD ["node", "app.js"]

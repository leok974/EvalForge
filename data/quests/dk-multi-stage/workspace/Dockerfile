# Single-stage build — works but ships a bloated image with dev deps included.
# Refactor this into a two-stage build:
#   Stage 1 (builder): install deps and compile/build
#   Stage 2 (runtime): copy only the built output from stage 1

FROM node:18
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
RUN npm run build
CMD ["node", "dist/index.js"]

import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

const lines = () =>
    fs.readFileSync(path.join(WS, "Dockerfile"), "utf8")
        .split("\n")
        .map((l) => l.trim())
        .filter((l) => l && !l.startsWith("#"));

test("Dockerfile meets required instructions", () => {
    const L = lines().join("\n");

    assert.match(L, /^FROM node:20-alpine/m, "EF_INFRA_DOCKER_FROM: require FROM node:20-alpine");
    assert.match(L, /^WORKDIR \/app/m, "EF_INFRA_DOCKER_WORKDIR: require WORKDIR /app");
    assert.match(L, /^RUN npm ci/m, "EF_INFRA_DOCKER_NPM_CI: require RUN npm ci");
    assert.match(L, /^EXPOSE 8000/m, "EF_INFRA_DOCKER_EXPOSE: require EXPOSE 8000");
    assert.match(L, /^CMD \["node","server\.js"\]/m, "EF_INFRA_DOCKER_CMD: require CMD [\"node\",\"server.js\"]");
});

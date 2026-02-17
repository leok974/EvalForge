import test from "node:test";
import { readText, mustContain, mustNotContain } from "./_h.mjs";

test("Compose Basics", () => {
    const t = readText("workspace/docker-compose.yml");
    mustNotContain(t, "TODO");
    
    mustContain(t, "services:");
    mustContain(t, "web:");
    mustContain(t, "3000:3000");
    mustContain(t, "NODE_ENV");
    mustContain(t, "production");
    mustContain(t, "restart:");
});

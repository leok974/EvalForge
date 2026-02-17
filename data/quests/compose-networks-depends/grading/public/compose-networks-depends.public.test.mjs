import test from "node:test";
import { readText, mustContain, mustNotContain } from "./_h.mjs";

test("Compose: Networks & depends_on", () => {
    const t = readText("workspace/docker-compose.yml");
    mustNotContain(t, "TODO");
    
    mustContain(t, "depends_on:");
    mustContain(t, "db:");
    mustContain(t, "networks:");
});

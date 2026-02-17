import test from "node:test";
import { readText, mustContain, mustNotContain, mustMatch } from "./_h.mjs";

test("Compose: Env & Secrets", () => {
    const t = readText("workspace/docker-compose.yml");
    mustNotContain(t, "TODO");
    
    mustContain(t, "env_file:");
    // Should NOT have inline passwords
    mustMatch(t, /^(?!.*PASSWORD=).*/sm, "Avoid inline PASSWORD env vars");
    
    mustContain(t, "secrets:");
});

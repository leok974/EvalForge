import test from "node:test";
import { readText, mustMatch } from "./_h.mjs";

test("Dockerfile: HEALTHCHECK", () => {
    const t = readText("workspace/Dockerfile");
    
    mustMatch(t, /^HEALTHCHECK\s/m, "Missing HEALTHCHECK instruction");
    mustMatch(t, /(curl|wget)/, "Healthcheck command should use curl or wget");
    mustMatch(t, /(\/health|\/ready)/, "Healthcheck path missing (/health or /ready)");
});

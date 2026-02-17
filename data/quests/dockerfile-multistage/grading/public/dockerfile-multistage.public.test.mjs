import test from "node:test";
import { readText, mustMatch } from "./_h.mjs";

test("Dockerfile: Multi-stage build", () => {
    const t = readText("workspace/Dockerfile");
    
    mustMatch(t, /AS builder/i, "Missing builder stage");
    mustMatch(t, /FROM .+ AS (runner|runtime)/i, "Missing runner/runtime stage");
    mustMatch(t, /COPY --from=builder/i, "Missing COPY --from=builder");
});

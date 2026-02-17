import test from "node:test";
import { readText, mustNotContain, mustMatch } from "./_h.mjs";

test("Dockerfile: COPY vs ADD", () => {
    const t = readText("workspace/Dockerfile");
    mustNotContain(t, "TODO");
    
    // Should NOT contain ADD (except in comments)
    // We check for "ADD " at start of line
    mustMatch(t, /^(?!.*^ADD\s).*/sm, "Should not use ADD instruction");
    
    // Should use COPY at least twice
    const copyCount = (t.match(/^COPY\s/gm) || []).length;
    if (copyCount < 2) throw new Error("Expected at least 2 COPY instructions");
});

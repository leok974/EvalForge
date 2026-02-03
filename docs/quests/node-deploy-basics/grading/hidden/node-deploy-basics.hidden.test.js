import test from "node:test";
import assert from "node:assert/strict";
import { server } from "../../starter/app.js";

let baseUrl;
test.before(async () => {
    await new Promise(resolve => server.listen(0, () => {
        baseUrl = `http://localhost:${server.address().port}`;
        resolve();
    }));
});

test.after(() => server.close());

test("GET /healthz returns 200 OK", async () => {
    const res = await fetch(`${baseUrl}/healthz`);
    assert.equal(res.status, 200, "EF_DEPLOY_HEALTH_STATUS: Should be 200");
    const text = await res.text();
    assert.match(text, /OK/, "EF_DEPLOY_HEALTH_BODY: Should return OK");
});

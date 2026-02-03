import test from "node:test";
import assert from "node:assert/strict";
import { server } from "../../starter/server.js";

let baseUrl;
test.before(async () => {
    await new Promise(resolve => server.listen(0, () => {
        baseUrl = `http://localhost:${server.address().port}`;
        resolve();
    }));
});

test.after(() => server.close());

test("GET /error returns 500", async () => {
    const res = await fetch(`${baseUrl}/error`);
    assert.equal(res.status, 500, "EF_HTTP_ERROR_STATUS: Should be 500");
});

test("GET /unknown returns 404", async () => {
    const res = await fetch(`${baseUrl}/random-path-xyz`);
    assert.equal(res.status, 404, "EF_HTTP_404_STATUS: Should be 404");
});

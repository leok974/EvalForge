import test from "node:test";
import assert from "node:assert/strict";
import { server } from "../../starter/server.js";

// Helper to make requests to our in-memory server
function request(path) {
    return new Promise((resolve, reject) => {
        server.listen(0, () => { // Random port
            const port = server.address().port;
            const req = fetch(`http://localhost:${port}${path}`)
                .then(async (res) => {
                    const text = await res.text();
                    return { status: res.status, headers: res.headers, text };
                })
                .then(resolve)
                .catch(reject)
                .finally(() => server.close());
        });
    });
}
// Actually, starting/stopping server for EACH request is slow/race-prone if not careful.
// Better: Start once before tests, close after.

let baseUrl;
test.before(async () => {
    await new Promise(resolve => server.listen(0, () => {
        baseUrl = `http://localhost:${server.address().port}`;
        resolve();
    }));
});

test.after(() => server.close());

test("GET / returns 200 Hello World", async () => {
    const res = await fetch(`${baseUrl}/`);
    assert.equal(res.status, 200, "EF_HTTP_ROOT_STATUS: Should be 200");
    const text = await res.text();
    assert.equal(text, "Hello World", "EF_HTTP_ROOT_BODY: Body should match");
});

test("GET /api returns JSON", async () => {
    const res = await fetch(`${baseUrl}/api`);
    assert.equal(res.status, 200, "EF_HTTP_API_STATUS: Should be 200");
    assert.match(res.headers.get("content-type") || "", /application\/json/, "EF_HTTP_API_HEADER: Content-Type be json");
    const data = await res.json();
    assert.deepEqual(data, { message: "Hello API" }, "EF_HTTP_API_BODY: JSON body mismatch");
});

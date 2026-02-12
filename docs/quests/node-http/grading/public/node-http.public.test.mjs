import test from "node:test";
import assert from "node:assert/strict";
import { server } from "../../workspace/server.js";

let baseUrl;

test.before(async () => {
    await new Promise((resolve) =>
        server.listen(0, () => {
            baseUrl = `http://localhost:${server.address().port}`;
            resolve();
        })
    );
});

test.after(() => server.close());

test("GET / returns 200 Hello World", async () => {
    const res = await fetch(`${baseUrl}/`);
    assert.equal(res.status, 200, "EF_NODE_HTTP_ROOT_STATUS");
    assert.match(res.headers.get("content-type") || "", /text\/plain/i, "EF_NODE_HTTP_ROOT_CT");
    const text = await res.text();
    assert.equal(text, "Hello World", "EF_NODE_HTTP_ROOT_BODY");
});

test("GET /api returns JSON", async () => {
    const res = await fetch(`${baseUrl}/api`);
    assert.equal(res.status, 200, "EF_NODE_HTTP_API_STATUS");
    assert.match(res.headers.get("content-type") || "", /application\/json/i, "EF_NODE_HTTP_API_HEADER");
    const data = await res.json();
    assert.deepEqual(data, { message: "Hello API" }, "EF_NODE_HTTP_API_BODY");
});

test("GET /error returns 500", async () => {
    const res = await fetch(`${baseUrl}/error`);
    assert.equal(res.status, 500, "EF_NODE_HTTP_ERROR_STATUS");
});

test("Unknown route returns 404", async () => {
    const res = await fetch(`${baseUrl}/nope`);
    assert.equal(res.status, 404, "EF_NODE_HTTP_404_STATUS");
});

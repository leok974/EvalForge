import http from "node:http";

const PORT = 3000;

export const server = http.createServer((req, res) => {
    // TODO: Implement routing
    // 1. GET / -> 200 OK, text/plain, "Hello World"
    // 2. GET /api -> 200 OK, application/json, { message: "Hello API" }
    // 3. GET /error -> 500 Internal Server Error
    // 4. Other -> 404 Not Found

    res.end();
});

// Only listen if main module (for testing import vs execution)
// but simplistic approach:
if (process.argv[1] === new URL(import.meta.url).pathname) {
    server.listen(PORT, () => {
        console.log(`Server listening on port ${PORT}`);
    });
}

import http from "node:http";

const PORT = 3000;

export const server = http.createServer((req, res) => {
    if (req.method === "GET") {
        if (req.url === "/") {
            res.writeHead(200, { "Content-Type": "text/plain" });
            res.end("Hello World");
            return;
        }
        if (req.url === "/api") {
            res.writeHead(200, { "Content-Type": "application/json" });
            res.end(JSON.stringify({ message: "Hello API" }));
            return;
        }
        if (req.url === "/error") {
            res.statusCode = 500;
            res.end("Internal Server Error");
            return;
        }
    }

    res.statusCode = 404;
    res.end("Not Found");
});

if (process.argv[1] === new URL(import.meta.url).pathname) {
    server.listen(PORT, () => {
        console.log(`Server listening on port ${PORT}`);
    });
}

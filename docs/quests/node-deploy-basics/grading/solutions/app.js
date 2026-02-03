import http from "node:http";

const PORT = process.env.PORT || 3000;

export const server = http.createServer((req, res) => {
    if (req.url === "/healthz") {
        res.writeHead(200);
        res.end("OK");
        return;
    }

    res.end("App Running");
});

if (process.argv[1] === new URL(import.meta.url).pathname) {
    server.listen(PORT, () => {
        console.log(`Server listening on port ${PORT}`);
    });
}

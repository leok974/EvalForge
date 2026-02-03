import http from "node:http";

// TODO: Use process.env.PORT, default to 3000
const PORT = 3000;

export const server = http.createServer((req, res) => {
    if (req.url === "/healthz") {
        // TODO: Respond with 200 'OK'
        // This is often used by cloud load balancers
        res.end("TODO");
        return;
    }

    res.end("App Running");
});

if (process.argv[1] === new URL(import.meta.url).pathname) {
    server.listen(PORT, () => {
        console.log(`Server listening on port ${PORT}`);
    });
}

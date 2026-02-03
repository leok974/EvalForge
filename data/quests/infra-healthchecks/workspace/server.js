import http from "node:http";

const port = Number(process.env.PORT || "0");

const server = http.createServer((req, res) => {
    // TODO: implement /health and /ready per README
    res.statusCode = 404;
    res.end("not_found");
});

server.listen(port, "127.0.0.1", () => {
    const addr = server.address();
    const p = typeof addr === "object" && addr ? addr.port : port;
    console.log(`PORT ${p}`);
});

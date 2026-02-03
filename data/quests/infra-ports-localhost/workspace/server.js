import http from "node:http";

const port = Number(process.env.PORT || "8000");
const server = http.createServer((req, res) => {
    res.statusCode = 200;
    res.end("ok");
});

// TODO: bind to 0.0.0.0 and log LISTEN <port>
server.listen(port, "127.0.0.1");

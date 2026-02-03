import http from "node:http";

const port = Number(process.env.PORT || "8000");
const server = http.createServer((req, res) => {
    res.statusCode = 200;
    res.end("ok");
});

server.listen(port, "0.0.0.0", () => {
    const addr = server.address();
    const p = typeof addr === "object" && addr ? addr.port : port;
    console.log(`LISTEN ${p}`);
});

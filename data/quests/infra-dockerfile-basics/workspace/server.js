import http from "node:http";

const port = Number(process.env.PORT || "8000");
const server = http.createServer((req, res) => {
    res.statusCode = 200;
    res.end("ok");
});
server.listen(port, "0.0.0.0", () => {
    console.log(`listening:${port}`);
});

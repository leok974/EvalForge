import http from "node:http";
import fs from "node:fs";
import path from "node:path";

const port = Number(process.env.PORT || "0");
const FLAG = path.join("fixtures", "ready.flag");

const server = http.createServer((req, res) => {
    if (req.url === "/health") {
        res.statusCode = 200;
        res.end("ok");
        return;
    }
    if (req.url === "/ready") {
        if (fs.existsSync(FLAG)) {
            res.statusCode = 200;
            res.end("ready");
        } else {
            res.statusCode = 503;
            res.end("not_ready");
        }
        return;
    }
    res.statusCode = 404;
    res.end("not_found");
});

server.listen(port, "127.0.0.1", () => {
    const addr = server.address();
    const p = typeof addr === "object" && addr ? addr.port : port;
    console.log(`PORT ${p}`);
});

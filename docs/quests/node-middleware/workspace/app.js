import http from "node:http";
import { requestLogger, authMiddleware, errorMiddleware } from "./middleware.js";

// Minimal middleware runner
function runMiddleware(req, res, middlewares, handler) {
    let index = 0;

    function next(err) {
        if (err) {
            return errorMiddleware(err, req, res, () => { });
        }
        if (index < middlewares.length) {
            const mw = middlewares[index++];
            try {
                mw(req, res, next);
            } catch (e) {
                next(e);
            }
        } else {
            try {
                handler(req, res);
            } catch (e) {
                next(e);
            }
        }
    }

    next();
}

export const server = http.createServer((req, res) => {
    runMiddleware(req, res, [requestLogger, authMiddleware], () => {
        if (req.url === "/error") {
            throw new Error("Boom");
        }
        res.end("Hello Secure World");
    });
});

if (process.argv[1] === new URL(import.meta.url).pathname) {
    server.listen(3000);
}

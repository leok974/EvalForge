export function requestLogger(req, res, next) {
    console.log(`${req.method} ${req.url}`);
    next();
}

export function authMiddleware(req, res, next) {
    if (req.headers['x-api-key'] === 'secret123') {
        next();
    } else {
        res.statusCode = 401;
        res.end("Unauthorized");
    }
}

export function errorMiddleware(err, req, res, next) {
    console.error(err);
    res.statusCode = 500;
    res.end("Internal Server Error");
}

export function requestLogger(req, res, next) {
    // TODO: Log "Method Path" (e.g., "GET /") using console.log
    // Then call next()
    next();
}

export function authMiddleware(req, res, next) {
    // TODO: Check if req.headers['x-api-key'] is "secret123"
    // If yes, call next()
    // If no, set res.statusCode = 401, res.end("Unauthorized"), and DO NOT call next()
    next();
}

export function errorMiddleware(err, req, res, next) {
    // TODO: Log the error message
    // Set status 500
    // End response with "Internal Server Error"
    next();
}

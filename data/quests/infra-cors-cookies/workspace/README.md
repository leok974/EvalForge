# Infra CORS & Cookies: Security Report

Read fixtures/request_origin.txt and fixtures/response_headers.txt.
Write outputs/security_report.txt with flags:

CORS_OK=true|false
CREDENTIALS=true|false
COOKIE_SECURE=true|false
COOKIE_SAMESITE=Lax|Strict|None|Unknown

Rules:
- CORS_OK=true if Access-Control-Allow-Origin matches request origin or *
- CREDENTIALS=true if Access-Control-Allow-Credentials is true
- COOKIE_SECURE=true if Set-Cookie contains Secure
- COOKIE_SAMESITE extract SameSite value or Unknown

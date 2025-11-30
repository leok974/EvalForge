# Changelog

All notable changes to EvalForge will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **DevDiag over HTTP**: Integrated automated UI diagnostics via HTTP proxy
  - Backend proxy router at `/api/ops/diag` that forwards to remote DevDiag HTTP service
  - Frontend client utility (`apps/web/src/lib/devdiag.ts`) with no JWT exposure
  - Health check endpoint at `/api/ops/diag/health`
  - Server-side JWT authentication (DEVDIAG_JWT env var)
  - 120s timeout with proper error propagation (429, 503, 504)
  - CI workflow integration for PR checks and hourly canary monitoring
  - Comprehensive documentation in `docs/devdiag.md`

### Changed
- Updated environment configuration to support DevDiag HTTP proxy
  - Added `DEVDIAG_BASE` (required in prod): Base URL of DevDiag HTTP server
  - Added `DEVDIAG_JWT` (optional): Bearer token for DevDiag authentication

### Security
- DevDiag JWT tokens now kept server-side only (never exposed to frontend)
- Frontend clients use backend proxy for all DevDiag operations

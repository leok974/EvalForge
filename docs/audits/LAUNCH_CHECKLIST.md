# EvalForge Launch Checklist

## Automated (all complete)

- [x] CI snapshot: `python scripts/ci_check_modern_worlds.py` — exit 0
- [x] `certify_training_grade.py` — exit 0
- [x] E2E suite: 8/8 worlds passing in parallel (~20s)
      `npx playwright test tests/e2e/test_foundry_quest.spec.ts tests/e2e/test_world_*.spec.ts`
- [x] Boss fight: operational (mock mode confirmed via e2e + manual API check)
- [x] Codex search: operational
- [x] Explain agent: operational
- [x] Security config: `EVALFORGE_AUTH_MODE=mock` and `EVALFORGE_MOCK_GRADING=1`
      are dev-only env vars — confirm they are NOT set in the production image/compose

## Manual (required before first real user)

- [ ] **GitHub OAuth:** Set `EVALFORGE_AUTH_MODE=github`, `GITHUB_CLIENT_ID`,
      and `GITHUB_CLIENT_SECRET` in `.env`; log in via browser; confirm session
      persists across page reload and that the user record is created in the DB.

- [ ] **SECRET_KEY:** Replace the placeholder in `.env` with a real 32-char
      random value:
      ```
      openssl rand -hex 32
      ```

- [ ] **Postgres password:** Change `evalforge:evalforge` in `docker-compose.yml`
      to a real credential before any public-facing deployment.

- [ ] **GOOGLE_CLOUD_PROJECT:** Set the real project ID if Gemini-backed boss
      grading is needed. Not required for mock-mode launch
      (`EVALFORGE_MOCK_GRADING=1`).

## Post-launch (first week)

- [ ] Monitor quest completion rates per track — drop-offs indicate content gaps.
- [ ] Monitor boss fight submission rate — a low rate may mean learners are not
      reaching track ends.
- [ ] Run `python scripts/ci_check_modern_worlds.py` weekly as a cron job to
      catch content regressions early.

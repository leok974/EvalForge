# Infra Debug Playbook: Next Steps

Read fixtures/diag.txt (key=value).
Check SYMPTOM value.

Write outputs/next_steps.txt with 3 specific diagnostic steps based on SYMPTOM.

Cases:
- SYMPTOM=502 -> Proxy/Upstream steps
- SYMPTOM=401 -> Auth steps
- SYMPTOM=CORS -> CORS steps
- Anything else -> Generic steps

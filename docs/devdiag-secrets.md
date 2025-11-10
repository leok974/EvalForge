# DevDiag GitHub Secrets Configuration

The DevDiag integration requires the following GitHub repository secrets to be configured for CI workflows:

## Required Secrets

### `DEVDIAG_BASE`
- **Description**: Base URL of the MCP DevDiag server
- **Example**: `https://devdiag.example.com` or `http://localhost:8023`
- **Used by**: `devdiag-quickcheck.yml`, `devdiag-canary.yml`
- **Purpose**: API endpoint for running diagnostics

### `DEVDIAG_READER_JWT`
- **Description**: JWT token with read-only permissions for running diagnostics
- **Permissions**: Can call `/mcp/diag/quickcheck` endpoint
- **Used by**: `devdiag-quickcheck.yml`, `devdiag-canary.yml`
- **Purpose**: Authenticate diagnostic requests
- **How to get**: Generate from DevDiag server's JWKS configuration

### `DEVDIAG_OPERATOR_JWT`
- **Description**: JWT token with write permissions for learning/remediation
- **Permissions**: Can call `/mcp/diag/remediation` endpoint
- **Used by**: Future learning workflows
- **Purpose**: Record successful fixes for AI learning
- **How to get**: Generate from DevDiag server's JWKS configuration with operator claims

### `EVALFORGE_PREVIEW_URL`
- **Description**: URL pattern for PR preview environments
- **Example**: `https://preview-{pr}.evalforge.int` or `https://evalforge-pr-{pr}.herokuapp.com`
- **Used by**: `devdiag-quickcheck.yml`
- **Purpose**: Target URL for PR diagnostic checks
- **Note**: Use `{pr}` placeholder for PR number substitution

### `EVALFORGE_CANARY_URL`
- **Description**: Production or staging URL for hourly health checks
- **Default**: `https://evalforge.app/healthz`
- **Used by**: `devdiag-canary.yml`
- **Purpose**: Continuous production monitoring

## Setting Secrets

### Via GitHub UI
1. Go to repository **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Enter name (e.g., `DEVDIAG_BASE`) and value
4. Click **Add secret**
5. Repeat for all secrets

### Via GitHub CLI
```bash
gh secret set DEVDIAG_BASE --body "https://devdiag.example.com"
gh secret set DEVDIAG_READER_JWT --body "eyJhbGc..."
gh secret set DEVDIAG_OPERATOR_JWT --body "eyJhbGc..."
gh secret set EVALFORGE_PREVIEW_URL --body "https://preview-{pr}.evalforge.int"
gh secret set EVALFORGE_CANARY_URL --body "https://evalforge.app/healthz"
```

## Local Development

For local testing (not CI), set environment variables in `.env`:

```bash
# DevDiag Server
DEVDIAG_BASE=http://localhost:8023
DEVDIAG_JWT=your_reader_token_here
DEVDIAG_OPERATOR_JWT=your_operator_token_here

# For testing workflows locally (act or similar)
EVALFORGE_PREVIEW_URL=http://localhost:5173
EVALFORGE_CANARY_URL=http://localhost:19010/healthz
```

## Generating JWT Tokens

If your DevDiag server uses JWKS authentication:

1. **Generate RSA key pair** (if not already done):
   ```bash
   ssh-keygen -t rsa -b 4096 -m PEM -f devdiag.key
   ssh-keygen -f devdiag.key.pub -e -m PKCS8 > devdiag.pub
   ```

2. **Create JWT with claims**:
   ```python
   import jwt
   from datetime import datetime, timedelta
   
   # Reader token (read-only)
   reader_payload = {
       "sub": "github-actions",
       "role": "reader",
       "tenant": "evalforge",
       "exp": datetime.utcnow() + timedelta(days=365)
   }
   reader_token = jwt.encode(reader_payload, private_key, algorithm="RS256")
   
   # Operator token (read + write)
   operator_payload = {
       "sub": "github-actions",
       "role": "operator",
       "tenant": "evalforge",
       "exp": datetime.utcnow() + timedelta(days=365)
   }
   operator_token = jwt.encode(operator_payload, private_key, algorithm="RS256")
   ```

3. **Update `ops/devdiag.yaml`** with public key JWKS endpoint

## Security Notes

- **Never commit secrets to version control**
- Use separate tokens for CI (reader) vs manual operations (operator)
- Rotate tokens periodically (recommended: every 90 days)
- Reader tokens should have minimal permissions (quickcheck only)
- Operator tokens should be closely guarded (can write to learning database)
- For local dev, RBAC can be disabled in `ops/devdiag.yaml` (commented out by default)

## Workflow Behavior

### PR Quickcheck (`devdiag-quickcheck.yml`)
- **Triggers**: On PR open/update
- **Uses**: `DEVDIAG_BASE`, `DEVDIAG_READER_JWT`, `EVALFORGE_PREVIEW_URL`
- **Success**: Posts comment with diagnostic results
- **Failure**: Fails CI check, blocks merge

### Hourly Canary (`devdiag-canary.yml`)
- **Triggers**: Cron schedule (hourly at :07)
- **Uses**: `DEVDIAG_BASE`, `DEVDIAG_READER_JWT`, `EVALFORGE_CANARY_URL`
- **Success**: Closes any open canary alert issues
- **Failure**: Creates GitHub issue with `canary-alert` label

## Troubleshooting

### "401 Unauthorized" errors
- Check JWT token is valid and not expired
- Verify JWKS public key matches private key used to sign token
- Ensure token has correct claims (tenant, role)

### "Context access might be invalid" lint warnings
- These are false positives from GitHub Actions YAML linter
- The secrets will work correctly when workflow runs
- You can safely ignore these warnings

### Workflow not running
- Verify secrets are set (GitHub UI or `gh secret list`)
- Check workflow file syntax (Actions tab will show parse errors)
- For cron workflows, ensure repo has recent activity (GitHub pauses inactive repos)

## References

- [MCP DevDiag Documentation](https://github.com/modelcontextprotocol/devdiag)
- [GitHub Actions Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [JWT.io Debugger](https://jwt.io/) - Decode tokens to verify claims

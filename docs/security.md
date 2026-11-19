# Security

## Principles applied

- Least privilege: only `roles/logging.viewer`.
- No secrets in source: `.tfvars` and key files are gitignored.
- Non-root container user.
- Minimal runtime image; build tools only in builder stage.
- Input validation and escaping of filter values.
- Headless rendering (no display server).
- Dependency and container scanning in `make security`.

## Scanning

```bash
make security
```

Runs: ruff, bandit, pip-audit, detect-secrets, gitleaks, trivy (fs + image), checkov, terraform fmt/validate, hadolint.

## Reporting vulnerabilities

Please report security issues privately to the maintainer; do not open public issues for undisclosed vulnerabilities.
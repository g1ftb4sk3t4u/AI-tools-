# GitHub Deployment Guide

## Quick Deploy to GitHub

### 1. Create GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. Repository name: `intel-terminal`
3. Description: `Personal SIGINT Dashboard - IRC-style RSS feed monitor with Discord alerts`
4. Choose **Private** (for intelligence/security)
5. Click "Create repository"

### 2. Push Local Code

```bash
cd e:\Github\AI-tools\intel-terminal

# Add GitHub remote
git remote add origin https://github.com/YOUR_USERNAME/intel-terminal.git

# Push to main
git branch -M main
git push -u origin main
```

### 3. GitHub Actions (Optional CI/CD)

Create `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -r backend/requirements.txt
      - run: python -m pytest backend/tests/
```

### 4. Setup Secrets (For Production)

On GitHub → Settings → Secrets and variables:

```
DISCORD_WEBHOOK_URL = your_webhook_url
DATABASE_URL = your_db_url
```

Then use in workflows/deployment with `${{ secrets.DISCORD_WEBHOOK_URL }}`

---

Done! Your code is now versioned and shareable.

# FixEnv Mini

**Catch Python dependency conflicts, missing version pins, and CVEs in any GitHub repo — in seconds.**

[![npm](https://img.shields.io/npm/v/fixenv-cli.svg)](https://www.npmjs.com/package/fixenv-cli)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](#license)

🌐 **Try it now:** [fixenvmini.lovable.app](https://fixenvmini.lovable.app)

---

## What is FixEnv Mini?

FixEnv Mini scans a Python repository's dependency files (`requirements.txt`, `pyproject.toml`, `Pipfile`, `setup.py`, and lockfiles), detects conflicts and known vulnerabilities, and produces a portable **`.zfix`** snapshot you can use to reproduce a working environment.

It uses Google Gemini to recognize 25+ real-world dependency conflict patterns and OSV.dev for CVE detection.

---

## Three ways to use it

### 1. Web (no install)

Paste any public GitHub URL at **[fixenvmini.lovable.app](https://fixenvmini.lovable.app)**. Get a reproducibility score, issue list, and downloadable `.zfix` snapshot in under a minute.

### 2. CLI

```bash
# Scan a repo
npx fixenv-cli scan https://github.com/pallets/flask

# JSON output (for scripts / CI)
npx fixenv-cli scan https://github.com/pallets/flask --json
```

> 💡 A `pipx`-installable Python package is on the roadmap. For now the CLI is a thin Node wrapper around the same hosted API.

### 3. CI/CD (GitHub Actions)

Drop this into `.github/workflows/fixenv.yml` to fail builds on critical CVEs:

```yaml
name: FixEnv Security Check
on: [push, pull_request]

jobs:
  fixenv-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Run FixEnv Analysis
        run: |
          REPO_URL="https://github.com/${{ github.repository }}"
          npx fixenv-cli scan $REPO_URL --json > fixenv-report.json

      - name: Fail on Critical/High CVEs
        run: |
          COUNT=$(jq '.vulnerabilities | map(select(.severity=="CRITICAL" or .severity=="HIGH")) | length' fixenv-report.json)
          if [ "$COUNT" -gt 0 ]; then
            echo "❌ Found $COUNT critical/high vulnerabilities"
            exit 1
          fi

      - uses: actions/upload-artifact@v4
        with:
          name: fixenv-report
          path: fixenv-report.json
```

---

## Example output

```
🔧 FixEnv - Python Environment Analysis
──────────────────────────────────────────────────
Repository: pallets/flask
Python: ^3.8
Formats: Requirements.txt, Setup.py

📊 Reproducibility Score: 87%
⚠️  Issues Found: 3
🔒 Vulnerabilities: 1 (High)

Issues:
  ● Missing version pin: werkzeug (high)
  ● Outdated package: jinja2 (medium)
  ● Missing version pin: click (medium)

Security Vulnerabilities:
  🔴 GHSA-xxxx-xxxx-xxxx: requests@2.28.0 (HIGH)
     Fix: upgrade to 2.31.0
```

---

## What it detects

- **6 dependency formats** — `requirements.txt`, `pyproject.toml`, `poetry.lock`, `Pipfile`, `Pipfile.lock`, `setup.py`
- **25+ conflict patterns** — version pin gaps, breaking upgrades (e.g. SQLAlchemy 2.0 + Flask-SQLAlchemy <3), Python compatibility issues, deprecated packages, CUDA/torch mismatches, and more
- **CVEs** — real-time lookup against [OSV.dev](https://osv.dev) with CRITICAL / HIGH / MEDIUM / LOW ratings
- **Python version mismatches** — detected from `pyproject.toml`, `.python-version`, `runtime.txt`, and CI workflows
- **Reproducibility score** — single 0–100 number summarizing environment stability

---

## FAQ

**Why `npx` and not `pip`?**
The CLI is currently a Node wrapper around our hosted API — nothing about it requires Python locally, which made it fast to ship. A `pipx`-installable Python package is on the roadmap so Python users can use idiomatic tooling.

**Is my code sent to a server?**
Only public dependency files (e.g. `requirements.txt`) are fetched from GitHub for analysis — never your source code. Analysis runs on a hosted backend (Lovable Cloud + Google Gemini). For privacy-sensitive workflows, see the roadmap below.

**Does it work on private repos?**
Not in the current MVP — only public GitHub repos. Private repo support and a local-first mode are on the roadmap.

**What's a `.zfix` file?**
A portable JSON snapshot containing your fixed dependency file, the reproducibility score, detected issues, suggested fixes, and metadata. It's designed to be shareable and re-applicable to recreate a working environment.

**Who built this?**
Solo project by Reddy. Questions / feedback: **che10guduru@gmail.com**.

---

## Roadmap

- [ ] `pipx install fixenv` — native Python CLI
- [ ] **Local-first mode** — run dependency parsing and OSV lookups entirely on your machine; AI analysis becomes opt-in
- [ ] **MCP / Claude Code skill** — invoke FixEnv as a tool from your coding agent (no hosted server involved)
- [ ] Private repo support (GitHub token auth)
- [ ] Self-hostable Docker image

---

## Architecture

This is a React + Vite frontend with serverless edge functions for analysis. Full architecture, edge function specs, database schema, and AI prompt details live in **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)**.

---

## License

MIT

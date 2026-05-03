## Goal
Make the GitHub README user-facing. Move existing internal docs into `docs/ARCHITECTURE.md` so engineers landing on the repo immediately understand what FixEnv is and how to use it.

## Changes

### 1. New `README.md` (top-level, replaces current)
User-facing, scannable, ~150 lines. Structure:

- **Header** — name, one-line tagline, badges (npm version, license), link to live app (https://fixenvmini.lovable.app).
- **What is FixEnv Mini?** — 2–3 sentences: scans Python repos for dependency conflicts, missing pins, CVEs, and reproducibility issues; outputs a portable `.zfix` snapshot.
- **Three ways to use it:**
  1. **Web** — paste a GitHub URL at fixenvmini.lovable.app (no install).
  2. **CLI** — `npx fixenv-cli scan <repo-url>` (with note: "Python `pipx` package coming soon").
  3. **CI/CD** — copy-paste GitHub Actions snippet (the one already in the Footer dialog).
- **Example output** — the terminal block already in `cli/README.md` (Reproducibility Score, Issues, Vulnerabilities).
- **What it detects** — short bullet list: 6 dependency formats, 25+ conflict patterns, OSV.dev CVEs, Python version mismatches.
- **FAQ** — 4–5 entries:
  - *Why npx and not pip?* Honest answer + roadmap note.
  - *Is my code sent to a server?* Yes — hosted MVP. Only dependency files (not source) are fetched from public GitHub. Roadmap: local-first Python package + MCP skill.
  - *Does it work on private repos?* Not yet — public GitHub only in MVP.
  - *What's a `.zfix` file?* Portable JSON snapshot with fixed deps + metadata.
  - *Who built this?* Contact: che10guduru@gmail.com.
- **Roadmap** — short bullets: pipx package, local-first mode, MCP/Claude Code skill, private repo support.
- **Architecture** — one-liner: "See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)."
- **License** — MIT.

### 2. New `docs/ARCHITECTURE.md`
Move the current README content here essentially as-is:
- Architecture overview + flowchart
- Tech stack tables
- Page/route table
- Design system
- Edge functions detail (analyze-repo, generate-snapshot, create-share, get-share)
- Database schema + RLS notes
- Reproducibility score algorithm
- AI knowledge base (conflict patterns)
- File structure
- Configuration files
- User flow sequence diagram
- Performance optimizations

Add a one-line header pointing back to the user README.

### 3. No code changes
This is docs-only. No edits to `src/`, edge functions, CLI, or DB.

## Out of scope
- No pipx package in this change (separate task).
- No landing-page privacy section (separate task).
- No changes to `cli/README.md` (already user-facing and fine).

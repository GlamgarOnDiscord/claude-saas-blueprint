# Contributing to claude-saas-blueprint

Thanks for considering a contribution. This repo packages conventions, skills and hooks for AI coding agents — every change should make the workflow **more reliable** or **less verbose**, not just longer.

## Before opening a PR

1. **Run the integrity check** — must pass before commit:
   ```bash
   python scripts/verify-workflow-integrity.py
   ```
2. **Run the secret scan** :
   ```bash
   python scripts/scan_secrets.py --staged-only
   ```
3. **Validate hook scripts** (Windows) :
   ```powershell
   Get-ChildItem .claude/hooks/scripts/*.ps1 | ForEach-Object {
     $tokens = $null; $errors = $null
     [System.Management.Automation.Language.Parser]::ParseFile($_.FullName, [ref]$tokens, [ref]$errors) | Out-Null
     if ($errors.Count -gt 0) { Write-Error "$($_.Name) has parse errors" }
   }
   ```

## Conventions

- **AGENTS.md** is the single source of truth for cross-tool conventions. Avoid duplicating its content in `CLAUDE.md`.
- **CLAUDE.md** target ≤ 120 lines. Use rules and skills for detail.
- **Skills** : one folder per skill, `SKILL.md` with valid YAML frontmatter (see `docs/skills-conventions.md`).
- **Rules** : one file per domain (≤ 30 lines), inside `.claude/rules/`.
- **Hooks** : PowerShell-first on Windows, scripts in `.claude/hooks/scripts/`.

## Commit style

- One logical change per commit.
- Imperative mood : `Add ui-audit skill`, `Fix broken link in README`.
- Reference issues with `#NNN` when relevant.

## What we accept

- New skills that solve a recurring SaaS task with a clear when-to-use.
- Rules that codify a hard-learned lesson (with date in `_learned.md` if no domain fits).
- Hook improvements with concrete failure mode prevented.
- Doc fixes, dead-link removals, count corrections.

## What we don't accept

- Speculative skills "in case someone needs it".
- Dependencies pulled into the agent context for tasks that don't require them.
- Skills duplicating a bundled Claude Code skill (`/batch`, `/loop`, `/simplify`, `/debug`, `/claude-api`).

## License

By contributing, you agree your contribution will be licensed under the MIT License (see [LICENSE](./LICENSE)).

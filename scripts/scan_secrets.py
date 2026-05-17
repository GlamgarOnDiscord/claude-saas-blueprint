#!/usr/bin/env python3
"""
scan_secrets.py — Scanner de secrets dans le codebase (alternative légère à gitleaks).
Détecte les clés API, tokens, mots de passe hardcodés.

Usage : python scripts/scan_secrets.py [--staged-only] [--json]
  --staged-only : analyser uniquement les fichiers staged (git)
  --json        : output en JSON pour intégration CI
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
BOLD = "\033[1m"
RESET = "\033[0m"

@dataclass
class SecretRule:
    name: str
    pattern: str
    severity: str = "HIGH"  # HIGH | MEDIUM | LOW

    def compiled(self):
        return re.compile(self.pattern)


RULES: list[SecretRule] = [
    SecretRule("OpenAI API Key", r"sk-[a-zA-Z0-9]{20,}", "HIGH"),
    SecretRule("Anthropic API Key", r"sk-ant-[a-zA-Z0-9\-]{20,}", "HIGH"),
    SecretRule("AWS Access Key", r"AKIA[0-9A-Z]{16}", "HIGH"),
    SecretRule("AWS Secret Key", r"(?i)aws.{0,20}secret.{0,20}['\"][0-9a-zA-Z/+=]{40}['\"]", "HIGH"),
    SecretRule("GitHub Token", r"ghp_[a-zA-Z0-9]{36}", "HIGH"),
    SecretRule("GitHub OAuth App Secret", r"gho_[a-zA-Z0-9]{36}", "HIGH"),
    SecretRule("Supabase Service Role", r"service_role['\"]?\s*[:=]\s*['\"]ey[a-zA-Z0-9._-]{20,}", "HIGH"),
    SecretRule("Stripe Secret Key", r"sk_live_[a-zA-Z0-9]{24,}", "HIGH"),
    SecretRule("Stripe Publishable Key (prod)", r"pk_live_[a-zA-Z0-9]{24,}", "MEDIUM"),
    SecretRule("Slack Bot Token", r"xoxb-[0-9]+-[0-9]+-[a-zA-Z0-9]+", "HIGH"),
    SecretRule("SendGrid API Key", r"SG\.[a-zA-Z0-9\-_]{22}\.[a-zA-Z0-9\-_]{43}", "HIGH"),
    SecretRule("Twilio Auth Token", r"(?i)twilio.{0,20}['\"][0-9a-f]{32}['\"]", "HIGH"),
    SecretRule("ElevenLabs API Key", r"(?i)elevenlabs['\"]?\s*[:=]\s*['\"][a-zA-Z0-9]{32,}", "HIGH"),
    SecretRule("Generic JWT Secret", r"(?i)jwt.{0,10}secret.{0,10}['\"][^'\"]{16,}['\"]", "MEDIUM"),
    SecretRule("Database URL with password", r"postgresql://[^:]+:[^@]{6,}@", "HIGH"),
    SecretRule("Hardcoded password", r"(?i)password\s*[:=]\s*['\"][^'\"]{8,}['\"]", "MEDIUM"),
    SecretRule("Private key block", r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", "HIGH"),
]

SKIP_DIRS = {".git", "node_modules", ".next", "dist", "build", ".turbo", "coverage"}
SKIP_FILES = {".env.example", "scan_secrets.py", "pre_deploy_check.py"}
SCAN_EXTENSIONS = {
    ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs",
    ".py", ".go", ".rb", ".php",
    ".json", ".yaml", ".yml", ".toml",
    ".env", ".sh", ".bash",
}


@dataclass
class Finding:
    file: str
    line: int
    rule: str
    severity: str
    snippet: str


def get_staged_files() -> list[Path]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        cwd=ROOT, capture_output=True, text=True
    )
    if result.returncode != 0:
        return []
    return [ROOT / f.strip() for f in result.stdout.splitlines() if f.strip()]


def scan_file(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return findings

    for rule in RULES:
        compiled = rule.compiled()
        for i, line in enumerate(content.splitlines(), 1):
            if compiled.search(line):
                # Masquer la valeur dans le snippet
                snippet = line.strip()[:120]
                findings.append(Finding(
                    file=str(path.relative_to(ROOT)),
                    line=i,
                    rule=rule.name,
                    severity=rule.severity,
                    snippet=snippet,
                ))
    return findings


def scan_directory(paths: list[Path] | None = None) -> list[Finding]:
    all_findings: list[Finding] = []

    if paths is not None:
        files = [p for p in paths if p.is_file()]
    else:
        files = []
        for path in ROOT.rglob("*"):
            if not path.is_file():
                continue
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            if path.name in SKIP_FILES:
                continue
            if path.suffix not in SCAN_EXTENSIONS and path.name not in {".env", ".env.local"}:
                continue
            files.append(path)

    for f in files:
        all_findings.extend(scan_file(f))

    return all_findings


def main() -> None:
    parser = argparse.ArgumentParser(description="Scanner de secrets")
    parser.add_argument("--staged-only", action="store_true",
                        help="Scanner uniquement les fichiers staged")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    if args.staged_only:
        staged = get_staged_files()
        if not staged:
            if not args.json:
                print(f"{GREEN}Aucun fichier staged.{RESET}")
            sys.exit(0)
        findings = scan_directory(staged)
    else:
        findings = scan_directory()

    if args.json:
        print(json.dumps([
            {"file": f.file, "line": f.line, "rule": f.rule, "severity": f.severity}
            for f in findings
        ], indent=2))
        sys.exit(1 if findings else 0)

    print(f"\n{BOLD}=== Scan Secrets ==={RESET}")
    print(f"  Mode : {'staged uniquement' if args.staged_only else 'codebase complet'}")

    if not findings:
        print(f"\n{GREEN}✓ Aucun secret détecté.{RESET}\n")
        sys.exit(0)

    # Grouper par sévérité
    high = [f for f in findings if f.severity == "HIGH"]
    medium = [f for f in findings if f.severity == "MEDIUM"]

    if high:
        print(f"\n{RED}{BOLD}CRITIQUE — {len(high)} secret(s) HIGH détecté(s) :{RESET}")
        for f in high:
            print(f"  {RED}✗{RESET} [{f.rule}] {f.file}:{f.line}")
            print(f"    {f.snippet[:80]}...")

    if medium:
        print(f"\n{YELLOW}ATTENTION — {len(medium)} secret(s) MEDIUM :{RESET}")
        for f in medium:
            print(f"  {YELLOW}⚠{RESET} [{f.rule}] {f.file}:{f.line}")

    print(f"\n{RED}ECHEC — {len(findings)} secret(s) trouvé(s). Commit bloqué.{RESET}\n")
    sys.exit(1)


if __name__ == "__main__":
    main()

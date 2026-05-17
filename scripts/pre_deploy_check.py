#!/usr/bin/env python3
"""
pre_deploy_check.py — Checks obligatoires avant tout déploiement Vercel/Supabase.
Usage : python scripts/pre_deploy_check.py [--env staging|production]
Retourne exit 0 si tout est OK, exit 1 si un check échoue.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

SECRET_PATTERNS = [
    r"sk-[a-zA-Z0-9]{20,}",          # OpenAI / generic SK
    r"AKIA[0-9A-Z]{16}",              # AWS Access Key
    r"ghp_[a-zA-Z0-9]{36}",          # GitHub Personal Access Token
    r"xoxb-[0-9]+-[a-zA-Z0-9]+",     # Slack Bot Token
    r"['\"]password['\"]\s*:\s*['\"][^'\"]{6,}['\"]",  # hardcoded password
    r"service_role['\"]?\s*[:=]\s*['\"]ey",  # Supabase service role
]

BLOCKED_EXTENSIONS = {".env", ".pem", ".key", ".p12", ".pfx"}


def run(cmd: list[str], cwd: Path = ROOT) -> tuple[int, str, str]:
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


def check(label: str, ok: bool, detail: str = "") -> bool:
    status = f"{GREEN}✓{RESET}" if ok else f"{RED}✗{RESET}"
    print(f"  {status} {label}", f"— {detail}" if detail else "")
    return ok


def check_typescript() -> bool:
    if not (ROOT / "tsconfig.json").exists():
        return check("TypeScript", True, "pas de tsconfig.json — skip")
    code, _, err = run(["npx", "tsc", "--noEmit"])
    return check("TypeScript (tsc --noEmit)", code == 0, err.strip()[:200] if err.strip() else "")


def check_lint() -> bool:
    pkg = ROOT / "package.json"
    if not pkg.exists():
        return check("Lint", True, "pas de package.json — skip")
    data = json.loads(pkg.read_text())
    if "lint" not in data.get("scripts", {}):
        return check("Lint", True, "pas de script lint — skip")
    pm = "pnpm" if (ROOT / "pnpm-lock.yaml").exists() else "npm"
    code, _, err = run([pm, "run", "lint"])
    return check("Lint", code == 0, err.strip()[:200] if code != 0 else "")


def check_tests() -> bool:
    pkg = ROOT / "package.json"
    if not pkg.exists():
        return check("Tests", True, "pas de package.json — skip")
    data = json.loads(pkg.read_text())
    if "test" not in data.get("scripts", {}):
        return check("Tests", True, "pas de script test — skip")
    pm = "pnpm" if (ROOT / "pnpm-lock.yaml").exists() else "npm"
    code, out, _ = run([pm, "run", "test", "--", "--passWithNoTests"])
    return check("Tests", code == 0, out.strip()[-150:] if code != 0 else "")


def check_secrets() -> bool:
    issues: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix in BLOCKED_EXTENSIONS and path.name != ".env.example":
            issues.append(f"fichier sensible détecté : {path.relative_to(ROOT)}")
            continue
        skip_dirs = {".git", "node_modules", ".next", "dist", "build", ".claude"}
        if any(part in skip_dirs for part in path.parts):
            continue
        if path.suffix not in {".ts", ".tsx", ".js", ".jsx", ".py", ".env", ".json", ".yaml", ".yml"}:
            continue
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for pattern in SECRET_PATTERNS:
            if re.search(pattern, content):
                issues.append(f"pattern secret dans {path.relative_to(ROOT)}")
                break
    ok = len(issues) == 0
    detail = "; ".join(issues[:3]) if issues else ""
    return check("Pas de secrets dans le code", ok, detail)


def check_env_vars() -> bool:
    example = ROOT / ".env.example"
    if not example.exists():
        return check("Variables d'env (.env.example)", True, "pas de .env.example — skip")
    lines = [l.strip() for l in example.read_text().splitlines() if "=" in l and not l.startswith("#")]
    keys = [l.split("=")[0] for l in lines]
    missing = [k for k in keys if not k.startswith("NEXT_PUBLIC_") and len(k) > 2]
    # On vérifie juste que le fichier est cohérent (pas de doublons)
    dupes = [k for k in keys if keys.count(k) > 1]
    ok = len(dupes) == 0
    detail = f"doublons : {dupes[:3]}" if dupes else f"{len(keys)} variables documentées"
    return check(".env.example cohérent", ok, detail)


def check_console_logs() -> bool:
    issues: list[str] = []
    skip_dirs = {".git", "node_modules", ".next", "dist", "build", "scripts"}
    for path in ROOT.rglob("*.ts"):
        if any(part in skip_dirs for part in path.parts):
            continue
        if path.name.endswith(".d.ts"):
            continue
        content = path.read_text(encoding="utf-8", errors="ignore")
        for i, line in enumerate(content.splitlines(), 1):
            if "console.log(" in line and "// rtk-ignore" not in line:
                issues.append(f"{path.relative_to(ROOT)}:{i}")
    ok = len(issues) == 0
    detail = f"{len(issues)} occurrences — premiers: {', '.join(issues[:3])}" if issues else ""
    return check("Pas de console.log", ok, detail)


def check_migrations_supabase() -> bool:
    migrations_dir = ROOT / "supabase" / "migrations"
    if not migrations_dir.exists():
        return check("Migrations Supabase", True, "pas de dossier supabase/migrations — skip")
    files = sorted(migrations_dir.glob("*.sql"))
    if not files:
        return check("Migrations Supabase", True, "aucune migration trouvée")
    # Vérifier que les fichiers sont bien nommés (timestamp_name.sql)
    bad = [f.name for f in files if not re.match(r"^\d{14}_", f.name)]
    ok = len(bad) == 0
    detail = f"nommage incorrect : {bad[:3]}" if bad else f"{len(files)} migrations trouvées"
    return check("Migrations Supabase (nommage)", ok, detail)


def check_rls() -> bool:
    """Vérification basique que les migrations activent RLS."""
    migrations_dir = ROOT / "supabase" / "migrations"
    if not migrations_dir.exists():
        return check("RLS activé dans migrations", True, "skip — pas de supabase/migrations")
    rls_pattern = re.compile(r"ALTER TABLE .+ ENABLE ROW LEVEL SECURITY", re.IGNORECASE)
    tables_with_rls: set[str] = set()
    for f in migrations_dir.glob("*.sql"):
        content = f.read_text(encoding="utf-8", errors="ignore")
        tables_with_rls.update(rls_pattern.findall(content))
    ok = len(tables_with_rls) > 0
    detail = f"{len(tables_with_rls)} tables avec RLS" if ok else "aucun ALTER TABLE ... ENABLE ROW LEVEL SECURITY trouvé"
    return check("RLS dans migrations", ok, detail)


def main() -> None:
    parser = argparse.ArgumentParser(description="Pre-deploy checks")
    parser.add_argument("--env", choices=["staging", "production"], default="staging")
    args = parser.parse_args()

    print(f"\n{BOLD}=== Pre-Deploy Checks [{args.env.upper()}] ==={RESET}\n")

    results = [
        check_typescript(),
        check_lint(),
        check_tests(),
        check_secrets(),
        check_env_vars(),
        check_console_logs(),
        check_migrations_supabase(),
        check_rls(),
    ]

    passed = sum(results)
    total = len(results)
    print(f"\n{BOLD}Résultat : {passed}/{total} checks passés{RESET}")

    if passed < total:
        failed = total - passed
        print(f"{RED}{failed} check(s) échoué(s) — déploiement bloqué.{RESET}\n")
        sys.exit(1)
    else:
        print(f"{GREEN}Tous les checks sont OK — déploiement autorisé.{RESET}\n")


if __name__ == "__main__":
    main()

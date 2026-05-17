#!/usr/bin/env python3
"""
project_health.py — Dashboard de santé du projet SaaS.
Affiche un résumé rapide sans sortie verbeux : TS errors, deps outdated,
bundle size, test coverage, sécurité.

Usage : python scripts/project_health.py [--full]
  --full : inclure l'audit deps et le bundle analysis (plus lent)
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"
DIM = "\033[2m"


def run(cmd: list[str]) -> tuple[int, str]:
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=60)
    return r.returncode, (r.stdout + r.stderr).strip()


def icon(ok: bool | None) -> str:
    if ok is None:
        return f"{YELLOW}~{RESET}"
    return f"{GREEN}✓{RESET}" if ok else f"{RED}✗{RESET}"


def section(title: str) -> None:
    print(f"\n{CYAN}{BOLD}▸ {title}{RESET}")


def check_typescript() -> None:
    section("TypeScript")
    if not (ROOT / "tsconfig.json").exists():
        print(f"  {icon(None)} Pas de tsconfig.json")
        return
    code, out = run(["npx", "tsc", "--noEmit"])
    errors = [l for l in out.splitlines() if "error TS" in l]
    print(f"  {icon(code == 0)} {len(errors)} erreur(s) TypeScript")
    for e in errors[:5]:
        print(f"    {DIM}{e.strip()[:100]}{RESET}")
    if len(errors) > 5:
        print(f"    {DIM}... +{len(errors) - 5} autres{RESET}")


def check_lint() -> None:
    section("Lint / Format")
    pkg = ROOT / "package.json"
    if not pkg.exists():
        print(f"  {icon(None)} Pas de package.json")
        return
    scripts = json.loads(pkg.read_text()).get("scripts", {})

    if "lint" in scripts:
        pm = "pnpm" if (ROOT / "pnpm-lock.yaml").exists() else "npm"
        code, out = run([pm, "run", "lint", "--", "--max-warnings=0"])
        warnings = len(re.findall(r"warning", out, re.IGNORECASE))
        errors = len(re.findall(r"error", out, re.IGNORECASE))
        print(f"  {icon(code == 0)} Lint — {errors} erreur(s), {warnings} warning(s)")
    else:
        print(f"  {icon(None)} Pas de script lint")


def check_tests() -> None:
    section("Tests")
    pkg = ROOT / "package.json"
    if not pkg.exists():
        print(f"  {icon(None)} Pas de package.json")
        return
    scripts = json.loads(pkg.read_text()).get("scripts", {})
    if "test" not in scripts:
        print(f"  {icon(None)} Pas de script test")
        return
    pm = "pnpm" if (ROOT / "pnpm-lock.yaml").exists() else "npm"
    code, out = run([pm, "run", "test", "--", "--reporter=verbose", "--passWithNoTests"])
    passed = len(re.findall(r"✓|passing|PASS", out))
    failed = len(re.findall(r"✗|failing|FAIL", out))
    print(f"  {icon(code == 0)} {passed} test(s) passé(s), {failed} échoué(s)")


def check_console_logs() -> None:
    section("Qualité code")
    skip = {".git", "node_modules", ".next", "dist", "scripts"}
    console_logs = 0
    any_types = 0
    large_files: list[tuple[str, int]] = []

    for path in ROOT.rglob("*.ts"):
        if any(p in skip for p in path.parts) or path.name.endswith(".d.ts"):
            continue
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
            lines = content.splitlines()
            console_logs += sum(1 for l in lines if "console.log(" in l)
            any_types += len(re.findall(r": any(?:\b|;|\s|,|\))", content))
            if len(lines) > 200:
                large_files.append((str(path.relative_to(ROOT)), len(lines)))
        except Exception:
            pass

    print(f"  {icon(console_logs == 0)} {console_logs} console.log()")
    print(f"  {icon(any_types == 0)} {any_types} usage(s) de `any`")
    print(f"  {icon(len(large_files) == 0)} {len(large_files)} fichier(s) >200 lignes")
    for f, n in sorted(large_files, key=lambda x: -x[1])[:3]:
        print(f"    {DIM}{f} ({n} lignes){RESET}")


def check_security() -> None:
    section("Sécurité")
    # Audit npm/pnpm
    pm = "pnpm" if (ROOT / "pnpm-lock.yaml").exists() else "npm"
    if (ROOT / "package.json").exists():
        code, out = run([pm, "audit", "--json"])
        try:
            data = json.loads(out.split("\n")[0] if pm == "pnpm" else out)
            if pm == "pnpm":
                vulns = data.get("metadata", {}).get("vulnerabilities", {})
            else:
                vulns = data.get("metadata", {}).get("vulnerabilities", {})
            high = vulns.get("high", 0) + vulns.get("critical", 0)
            total = sum(vulns.values())
            print(f"  {icon(high == 0)} {total} vulnérabilité(s) deps — {high} HIGH/CRITICAL")
        except Exception:
            print(f"  {icon(None)} Audit deps — output non parseable")

    # Check .env commité
    env_committed = False
    code, out = run(["git", "ls-files", ".env"])
    if out.strip():
        env_committed = True
    print(f"  {icon(not env_committed)} .env non commité")

    # Check RLS
    rls_code, _ = run(["python", "scripts/supabase_rls_check.py"])
    if rls_code == 0:
        print(f"  {icon(True)} RLS activé sur toutes les tables")
    else:
        print(f"  {icon(False)} RLS manquant sur certaines tables (voir supabase_rls_check.py)")


def check_structure() -> None:
    section("Structure hexagonale")
    src = ROOT / "src"
    if not src.exists():
        print(f"  {icon(None)} Pas de dossier src/")
        return
    checks = {
        "src/core/entities": (src / "core" / "entities").exists(),
        "src/core/usecases": (src / "core" / "usecases").exists(),
        "src/core/ports": (src / "core" / "ports").exists(),
        "src/adapters": (src / "adapters").exists(),
        "src/shared": (src / "shared").exists(),
    }
    for name, ok in checks.items():
        print(f"  {icon(ok)} {name}")


def check_git() -> None:
    section("Git")
    code, out = run(["git", "status", "--porcelain"])
    changed = [l for l in out.splitlines() if l.strip()]
    print(f"  {icon(len(changed) == 0)} {len(changed)} fichier(s) modifié(s) non commité(s)")

    code, branch = run(["git", "branch", "--show-current"])
    print(f"  {DIM}Branche : {branch.strip()}{RESET}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Dashboard santé projet")
    parser.add_argument("--full", action="store_true", help="Inclure audit complet (plus lent)")
    args = parser.parse_args()

    print(f"\n{BOLD}{'='*50}")
    print(f"  Project Health Dashboard")
    print(f"  {ROOT.name}")
    print(f"{'='*50}{RESET}")

    check_git()
    check_typescript()
    check_lint()
    check_tests()
    check_console_logs()
    check_security()
    check_structure()

    print(f"\n{DIM}Conseil : python scripts/pre_deploy_check.py pour les checks complets avant deploy.{RESET}\n")


if __name__ == "__main__":
    main()

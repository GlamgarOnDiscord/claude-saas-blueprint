#!/usr/bin/env python3
"""
supabase_migrate.py — Wrapper simplifié pour les migrations Supabase.
Évite les commandes longues et filtre les outputs verbeux.

Usage:
  python scripts/supabase_migrate.py --env local        # Reset local + apply
  python scripts/supabase_migrate.py --env staging      # Push vers staging
  python scripts/supabase_migrate.py --env production   # Push vers production (confirmation requise)
  python scripts/supabase_migrate.py --new nom-migration  # Créer une nouvelle migration
  python scripts/supabase_migrate.py --diff             # Voir les changements en attente
  python scripts/supabase_migrate.py --status           # Lister les migrations appliquées
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Lignes de l'output Supabase à ignorer (trop verbeux, inutiles pour l'agent)
NOISE_PATTERNS = [
    "Connecting to",
    "Applying migration",
    "Finished supabase",
    "supabase start",
    "supabase stop",
    "Started supabase",
    "anon key:",
    "service_role key:",   # ne pas logger les clés
    "API URL:",
    "GraphQL URL:",
    "S3 Storage URL:",
    "DB URL:",
    "Studio URL:",
    "Inbucket URL:",
    "JWT secret:",
]


def run_supabase(args: list[str], confirm_production: bool = False) -> int:
    if confirm_production:
        answer = input(f"{YELLOW}⚠ Déploiement PRODUCTION — Confirmer ? (oui/non) :{RESET} ")
        if answer.lower() not in ("oui", "o", "yes", "y"):
            print("Annulé.")
            return 0

    cmd = ["npx", "supabase"] + args
    print(f"{BOLD}$ {' '.join(cmd)}{RESET}")

    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)

    # Filtrer stdout
    filtered_lines = []
    for line in result.stdout.splitlines():
        if not any(noise in line for noise in NOISE_PATTERNS):
            filtered_lines.append(line)
    if filtered_lines:
        print("\n".join(filtered_lines))

    # Stderr uniquement si erreur
    if result.returncode != 0 and result.stderr:
        print(f"{RED}{result.stderr.strip()}{RESET}")

    return result.returncode


def cmd_new(name: str) -> int:
    safe_name = name.lower().replace(" ", "_").replace("-", "_")
    print(f"Création migration : {safe_name}")
    return run_supabase(["migration", "new", safe_name])


def cmd_diff() -> int:
    print(f"{BOLD}Diff du schéma (changements non migrés) :{RESET}")
    return run_supabase(["db", "diff", "--schema", "public"])


def cmd_status() -> int:
    print(f"{BOLD}Statut des migrations :{RESET}")
    return run_supabase(["migration", "list"])


def cmd_local() -> int:
    print(f"{BOLD}Reset local + application des migrations :{RESET}")
    return run_supabase(["db", "reset"])


def cmd_push(env: str) -> int:
    is_prod = env == "production"
    print(f"{BOLD}Push migrations → {env.upper()}{RESET}")
    # D'abord montrer le diff
    run_supabase(["db", "diff"])
    return run_supabase(["db", "push"], confirm_production=is_prod)


def main() -> None:
    parser = argparse.ArgumentParser(description="Supabase migration helper")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--env", choices=["local", "staging", "production"],
                       help="Environnement cible pour le push")
    group.add_argument("--new", metavar="NOM", help="Créer une nouvelle migration")
    group.add_argument("--diff", action="store_true", help="Voir les changements en attente")
    group.add_argument("--status", action="store_true", help="Lister les migrations")

    args = parser.parse_args()

    if args.new:
        sys.exit(cmd_new(args.new))
    elif args.diff:
        sys.exit(cmd_diff())
    elif args.status:
        sys.exit(cmd_status())
    elif args.env == "local":
        sys.exit(cmd_local())
    elif args.env in ("staging", "production"):
        sys.exit(cmd_push(args.env))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

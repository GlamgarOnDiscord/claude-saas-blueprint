#!/usr/bin/env python3
"""
rtk_setup.py — Installation et configuration de RTK (Rust Token Killer).
RTK réduit la consommation de tokens Claude Code de 60-90% en filtrant
les outputs verbeux des commandes (git, tests, lint, etc.).

GitHub : https://github.com/rtk-ai/rtk
Site   : https://www.rtk-ai.app/

Usage : python scripts/rtk_setup.py [--check] [--stats]
  --check : vérifier si RTK est installé et configuré
  --stats : afficher les économies de tokens (rtk gain)
"""
from __future__ import annotations

import argparse
import platform
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


def run(cmd: list[str]) -> tuple[int, str]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return r.returncode, (r.stdout + r.stderr).strip()
    except FileNotFoundError:
        return 127, "command not found"
    except Exception as e:
        return 1, str(e)


def is_rtk_installed() -> bool:
    code, _ = run(["rtk", "--version"])
    return code == 0


def get_rtk_version() -> str:
    code, out = run(["rtk", "--version"])
    return out.strip() if code == 0 else "non installé"


def check_rtk() -> None:
    print(f"\n{BOLD}=== État RTK ==={RESET}\n")
    installed = is_rtk_installed()
    version = get_rtk_version()

    if installed:
        print(f"  {GREEN}✓{RESET} RTK installé : {version}")
        code, out = run(["rtk", "status"])
        if code == 0:
            print(f"  {GREEN}✓{RESET} RTK actif")
            print(f"\n  {out}")
        else:
            print(f"  {YELLOW}⚠{RESET} RTK installé mais pas encore initialisé")
            print(f"    → Lancer : rtk init --global")
    else:
        print(f"  {RED}✗{RESET} RTK non installé")
        print(f"\n  Pour installer RTK :")
        _print_install_instructions()


def _print_install_instructions() -> None:
    os_name = platform.system().lower()

    print(f"\n  {CYAN}{BOLD}Installation RTK (Rust Token Killer){RESET}")
    print(f"  {CYAN}Réduit les tokens Claude Code de 60-90%{RESET}\n")

    if os_name == "darwin":
        print(f"  {BOLD}macOS :{RESET}")
        print(f"    brew install rtk-ai/tap/rtk")
        print(f"    # ou : curl -fsSL https://install.rtk-ai.app | sh")
    elif os_name == "linux":
        print(f"  {BOLD}Linux :{RESET}")
        print(f"    curl -fsSL https://install.rtk-ai.app | sh")
    elif os_name == "windows":
        print(f"  {BOLD}Windows :{RESET}")
        print(f"    winget install rtk-ai.rtk")
        print(f"    # ou PowerShell : iwr https://install.rtk-ai.app/win | iex")

    print(f"\n  {BOLD}Après installation :{RESET}")
    print(f"    rtk init --global    # Active le proxy sur toutes les commandes")
    print(f"    rtk gain             # Voir les économies de tokens")
    print(f"    rtk status           # Vérifier la configuration")

    print(f"\n  {BOLD}Ce que RTK optimise :{RESET}")
    commands = [
        ("git status / diff / log", "Filtre les diffs verbeux, garde l'essentiel"),
        ("pytest / cargo test / jest", "Résume les résultats de tests"),
        ("eslint / ruff / biome", "Compresse les rapports de lint"),
        ("pnpm install / npm ci", "Filtre les logs d'installation"),
        ("docker build / compose", "Résume les étapes de build"),
        ("tsc --noEmit", "Filtre les erreurs TypeScript"),
    ]
    for cmd, desc in commands:
        print(f"    {GREEN}✓{RESET} {cmd:<35} {desc}")

    print(f"\n  {BOLD}Intégration Claude Code :{RESET}")
    print(f"    RTK s'intègre automatiquement après `rtk init --global`.")
    print(f"    Les commandes Bash de Claude Code passeront par le proxy RTK.")
    print(f"    Aucune modification du workflow nécessaire.\n")


def show_stats() -> None:
    print(f"\n{BOLD}=== Statistiques RTK ==={RESET}\n")
    if not is_rtk_installed():
        print(f"  {RED}RTK non installé.{RESET}")
        return
    code, out = run(["rtk", "gain"])
    if code == 0:
        print(out)
    else:
        print(f"  {YELLOW}Pas de données disponibles.{RESET}")
        print(f"  Exécuter quelques commandes d'abord, puis relancer.")


def install_guide() -> None:
    print(f"\n{BOLD}=== Guide d'installation RTK ==={RESET}")
    _print_install_instructions()


def main() -> None:
    parser = argparse.ArgumentParser(description="Setup RTK - Rust Token Killer")
    parser.add_argument("--check", action="store_true", help="Vérifier le statut RTK")
    parser.add_argument("--stats", action="store_true", help="Afficher les stats de tokens")
    parser.add_argument("--install", action="store_true", help="Afficher le guide d'installation")
    args = parser.parse_args()

    if args.check:
        check_rtk()
    elif args.stats:
        show_stats()
    elif args.install:
        install_guide()
    else:
        # Mode par défaut : check + guide si non installé
        if is_rtk_installed():
            check_rtk()
            show_stats()
        else:
            print(f"\n{YELLOW}RTK non détecté.{RESET}")
            install_guide()
            sys.exit(1)


if __name__ == "__main__":
    main()

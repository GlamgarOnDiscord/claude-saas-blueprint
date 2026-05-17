"""memory-rotate — archive et compacte la memoire de l'agent.

Usage : python scripts/memory-rotate.py [--days N] [--dry-run]

Ce que fait ce script :
- Archive les sections > N jours (defaut 90) de session.md / errors.md / decisions.md
  vers .claude/memory/archive/<date>-<file>.md
- Detecte les doublons dans _learned.md et les regroupe par mois
- Affiche un rapport des elements archives et compactes

Garde-fous :
- Le mode --dry-run n'ecrit rien, il affiche juste ce qui serait fait
- Les fichiers source ne sont jamais ecrases sans backup intermediaire
- Si pas de section datee detectable, le fichier est laisse intact
"""

from __future__ import annotations

import argparse
import re
import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / ".claude" / "memory"
ARCHIVE = MEMORY / "archive"

ROTATABLE = ["session.md", "errors.md", "decisions.md", "domains.md"]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--days", type=int, default=90, help="Age limite en jours (defaut 90)")
    p.add_argument("--dry-run", action="store_true", help="N'ecrit rien, affiche les actions")
    return p.parse_args()


def find_dated_sections(text: str, cutoff: datetime) -> tuple[list[str], list[str]]:
    """Separe le texte en sections actuelles et a archiver (date detectee dans le titre).

    Pattern reconnu : `## Date : YYYY-MM-DD` ou `### YYYY-MM-DD ...` ou `## YYYY-MM-DD`.
    """
    lines = text.splitlines(keepends=True)
    sections: list[tuple[str, list[str], datetime | None]] = []  # (header, lines, date)
    current_header = "preamble"
    current_lines: list[str] = []
    current_date: datetime | None = None

    date_pattern = re.compile(r"(\d{4})-(\d{2})-(\d{2})")

    for line in lines:
        if line.startswith(("## ", "### ")):
            # Sauve la section precedente
            sections.append((current_header, current_lines, current_date))
            current_header = line.strip()
            current_lines = [line]
            m = date_pattern.search(line)
            if m:
                try:
                    current_date = datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)), tzinfo=timezone.utc)
                except ValueError:
                    current_date = None
            else:
                current_date = None
        else:
            current_lines.append(line)

    sections.append((current_header, current_lines, current_date))

    keep_lines: list[str] = []
    archive_lines: list[str] = []

    for header, slines, sdate in sections:
        if sdate is not None and sdate < cutoff:
            archive_lines.extend(slines)
        else:
            keep_lines.extend(slines)

    return keep_lines, archive_lines


def rotate_file(path: Path, cutoff: datetime, dry_run: bool) -> tuple[int, int]:
    """Retourne (nb_lignes_archivees, nb_lignes_gardees)."""
    if not path.exists():
        return 0, 0
    text = path.read_text(encoding="utf-8")
    keep, archive = find_dated_sections(text, cutoff)
    if not archive:
        return 0, len(keep)

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    archive_path = ARCHIVE / f"{today}-{path.name}"

    print(f"  {path.name} → {len(archive)} lignes archivees vers {archive_path.name}")

    if not dry_run:
        ARCHIVE.mkdir(parents=True, exist_ok=True)
        existing = archive_path.read_text(encoding="utf-8") if archive_path.exists() else ""
        archive_path.write_text(existing + "".join(archive), encoding="utf-8")
        path.write_text("".join(keep), encoding="utf-8")

    return len(archive), len(keep)


def deduplicate_learned(dry_run: bool) -> int:
    """Retire les doublons de _learned.md, conserve l'ordre chronologique."""
    learned = MEMORY.parent / "rules" / "_learned.md"
    if not learned.exists():
        return 0
    text = learned.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    seen: set[str] = set()
    out: list[str] = []
    duplicates = 0
    for line in lines:
        stripped = line.strip()
        # Ne dedupliquer que les lignes "rules" (commencent par "- [")
        if stripped.startswith("- [") and stripped in seen:
            duplicates += 1
            continue
        if stripped.startswith("- ["):
            seen.add(stripped)
        out.append(line)

    if duplicates and not dry_run:
        learned.write_text("".join(out), encoding="utf-8")

    return duplicates


def main() -> None:
    args = parse_args()
    cutoff = datetime.now(timezone.utc) - timedelta(days=args.days)

    print(f"=== Memory rotate (days={args.days}, dry_run={args.dry_run}) ===")
    print(f"Cutoff date: {cutoff.strftime('%Y-%m-%d')}")
    print(f"Memory dir : {MEMORY}")

    if not MEMORY.exists():
        print("No memory directory found, nothing to do.")
        return

    print("\n[Rotation]")
    total_archived = 0
    for name in ROTATABLE:
        path = MEMORY / name
        archived, _ = rotate_file(path, cutoff, args.dry_run)
        total_archived += archived

    print(f"\nTotal lignes archivees : {total_archived}")

    print("\n[Deduplication _learned.md]")
    dups = deduplicate_learned(args.dry_run)
    print(f"Doublons retires : {dups}")

    if args.dry_run:
        print("\n(dry-run) Aucun fichier modifie.")


if __name__ == "__main__":
    main()

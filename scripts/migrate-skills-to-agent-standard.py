#!/usr/bin/env python3
"""Migre .claude/skills/*.md vers skill-name/SKILL.md (norme Agent Skills)."""
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".claude" / "skills"


def parse_skill(text: str) -> tuple[str, str]:
    """Retourne (description_première_ligne, corps_markdown)."""
    text = re.sub(r"^#\s*Skill:\s*\S+\s*\n", "", text, count=1)
    m = re.match(r"^##\s+Description\s*\n(.*?)(?=\n##\s)", text, re.DOTALL)
    if not m:
        return "Skill du projet claude-saas-blueprint.", text.strip()
    desc_block = m.group(1).strip()
    first_line = desc_block.split("\n")[0].strip()
    rest = text[m.end() :].lstrip("\n")
    return first_line, rest.strip()


def yaml_escape(s: str) -> str:
    escaped = s.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def argument_hint(body: str) -> str | None:
    m = re.search(r"^##\s+Arguments\s*\n(.*?)(?=\n##\s|\Z)", body, re.DOTALL)
    if not m:
        return None
    lines = [ln.strip() for ln in m.group(1).strip().split("\n") if ln.strip().startswith("-")]
    if not lines:
        return None
    return " ".join(lines[:2])[:120]


def disable_auto(name: str) -> bool:
    """Skills déclenchés manuellement (effets de bord ou workflows lourds)."""
    return name in {
        "saas-init",
        "deploy-check",
        "migrate",
        "fork",
        "prd",
        "meta-prompt",
        "loop",
        "landing",
        "mcp-setup",
        "feature",
    }


def build_frontmatter(name: str, desc: str, body: str) -> str:
    lines = [
        "---",
        f"name: {name}",
        f'description: {yaml_escape(desc)}',
    ]
    hint = argument_hint(body)
    if hint:
        lines.append(f'argument-hint: "{hint}"')
    if disable_auto(name):
        lines.append("disable-model-invocation: true")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def main() -> None:
    # 1) Déplacer feature-steps → feature/steps
    old_steps = SKILLS / "feature-steps"
    new_steps = SKILLS / "feature" / "steps"
    if old_steps.is_dir():
        new_steps.mkdir(parents=True, exist_ok=True)
        for f in sorted(old_steps.glob("*.md")):
            dest = new_steps / f.name
            shutil.move(str(f), str(dest))
        old_steps.rmdir()

    # 2) Migrer chaque *.md à la racine de skills
    for f in sorted(SKILLS.glob("*.md")):
        name = f.stem
        text = f.read_text(encoding="utf-8")
        desc, body = parse_skill(text)
        if name == "feature":
            body = body.replace(
                ".claude/skills/feature-steps/",
                ".claude/skills/feature/steps/",
            )
        fm = build_frontmatter(name, desc, body)
        out_dir = SKILLS / name
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "SKILL.md").write_text(fm + body + "\n", encoding="utf-8")
        f.unlink()
        print(f"OK {name}/SKILL.md")

    print("Migration terminée.")


if __name__ == "__main__":
    main()

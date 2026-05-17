"""verify-workflow-integrity — verifie la coherence du dossier .claude/.

Checks :
- Skills : frontmatter YAML valide, etapes feature/ presentes, references croisees existantes.
- Liens markdown relatifs valides dans tout le repo.
- Compteurs (skills, rules, guides) coherents avec README/CLAUDE.md/MEMORY.md.
- References de skills `/...` dans les .md correspondent a un dossier reel.
- AGENTS.md contient les keywords cles (source unique conventions).
- Templates referencees au moins une fois.
- Hooks settings.json utilisent shell powershell (Windows-friendly).

Exit 0 si OK, 1 sinon. Lance via `python scripts/verify-workflow-integrity.py`.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


# ---------------------------------------------------------------------------
# Skill frontmatter
# ---------------------------------------------------------------------------

def is_valid_skill_frontmatter(text: str) -> tuple[bool, str]:
    if not text.startswith("---"):
        return False, "no-frontmatter-start"
    parts = text.split("---")
    if len(parts) < 3:
        return False, "frontmatter-parse"
    yaml_block = parts[1]
    if "name:" not in yaml_block:
        return False, "missing-name"
    if "description:" not in yaml_block:
        return False, "missing-description"
    return True, "ok"


# ---------------------------------------------------------------------------
# Markdown helpers
# ---------------------------------------------------------------------------

def extract_backticked_paths(text: str) -> list[str]:
    paths: list[str] = []
    for m in re.finditer(r"`([^`]+)`", text):
        candidate = m.group(1).strip()
        # Tronque a la premiere espace (ignore les arguments CLI)
        candidate = candidate.split()[0] if candidate else ""
        if any(candidate.startswith(prefix) for prefix in (
            "docs/", ".claude/", "platforms/", "templates/", "scripts/"
        )):
            paths.append(candidate)
    return paths


def extract_markdown_relative_links(text: str) -> list[str]:
    links: list[str] = []
    for m in re.finditer(r"\]\(([^)]+)\)", text):
        href = m.group(1).strip()
        if href.startswith(("http://", "https://", "#", "/", "mailto:")):
            continue
        href = href.split("#")[0].split("?")[0]
        if href:
            links.append(href)
    return links


def extract_slash_skills(text: str) -> set[str]:
    """Extrait toutes les references de slash skills (`/skill-name`).

    On ne capture que les `/skill` apparaissant :
    - dans une code-fence inline `/skill` ou `**/skill**`
    - apres un mot tel que "skill", "command", "lance", "invoque", "/`"
    - en debut de ligne ou de cellule de tableau
    On ignore les balises HTML (</tag>) et les chemins URL/files.
    """
    skills: set[str] = set()
    # Cas 1 : skill cite en `/nom` ou **`/nom`** (formattage markdown)
    for m in re.finditer(r"`/([a-z][a-z0-9-]+)`", text):
        skills.add(m.group(1))
    # Cas 2 : skill cite en italique/bold sans backtick : **/nom** ou */nom*
    for m in re.finditer(r"\*\*?/([a-z][a-z0-9-]+)\*\*?", text):
        skills.add(m.group(1))
    return skills


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def check_markdown_links(md_files: list[Path]) -> list[tuple[Path, str]]:
    broken: list[tuple[Path, str]] = []
    for md_file in md_files:
        text = read_text(md_file)
        for link in extract_markdown_relative_links(text):
            target = (md_file.parent / link).resolve()
            try:
                target.relative_to(ROOT.resolve())
            except Exception:
                continue
            if not target.exists():
                broken.append((md_file, link))
    return broken


def check_claude_md_line_count() -> tuple[int, bool]:
    claude_md = ROOT / "CLAUDE.md"
    if not claude_md.exists():
        return 0, False
    lines = read_text(claude_md).splitlines()
    count = len(lines)
    return count, count > 120


def check_agents_md_sync() -> list[str]:
    warnings: list[str] = []
    agents_md = ROOT / "AGENTS.md"
    if not agents_md.exists():
        warnings.append("AGENTS.md is missing — cross-tool portability reduced")
        return warnings
    text = read_text(agents_md)
    required_keywords = ["Hexagonal", "kebab-case", "PascalCase", "Zod", "organizationId", "APEX"]
    for kw in required_keywords:
        if kw not in text:
            warnings.append(f"AGENTS.md missing keyword: {kw}")
    return warnings


def check_templates_referenced() -> list[str]:
    unreferenced: list[str] = []
    templates_dir = ROOT / "templates"
    if not templates_dir.exists():
        return unreferenced

    all_text = ""
    for md_file in ROOT.rglob("*.md"):
        # On exclut chaque fichier template lui-meme, mais PAS le README templates/
        # qui sert d'index de reference.
        if md_file.is_relative_to(templates_dir) and md_file.name != "README.md":
            continue
        all_text += read_text(md_file) + "\n"

    for template_file in templates_dir.rglob("*.md"):
        basename = template_file.name
        if basename == "README.md":
            continue
        if basename not in all_text and template_file.stem not in all_text:
            unreferenced.append(str(template_file.relative_to(ROOT)))

    return unreferenced


def check_skill_references(skill_dirs: set[str]) -> list[tuple[Path, str]]:
    """Detecte les `/skill-name` cites dans les md mais sans dossier correspondant."""
    # Skills bundled Claude Code (existent en interne, pas de dossier ici).
    bundled = {
        "batch", "loop", "simplify", "debug", "claude-api",
        "memory", "compact", "skill",
        # Commandes Claude Code natives
        "init", "plugin", "permissions", "claude-md-prune",
        "agents", "model", "config", "review", "help",
        "save", "resume", "cost", "logout", "login",
        "doctor", "release-notes", "vim", "bug",
        "clear", "edit",
    }
    # Mots-cles qui ressemblent a un skill mais n'en sont pas (sections markdown, etc.)
    false_positives = {
        "us", "is", "a", "an", "or", "and", "to", "of", "the",
        "fr", "en", "var", "let", "const", "true", "false", "null",
        "this", "that", "with", "from", "for", "by",
        "tmp", "etc", "src", "lib", "app", "api", "var",
        "min", "max", "env", "next", "node", "ms", "url",
        "dev", "prod", "test", "ci", "cd", "fr-fr", "en-us",
        "nom", "usage", "effort", "public", "post-traitement",
        "health", "core", "adapters", "docs",
    }

    broken: list[tuple[Path, str]] = []
    for md_file in ROOT.rglob("*.md"):
        # Skip references/ dans les skills (deja interne)
        if "references" in md_file.parts:
            continue
        text = read_text(md_file)
        for skill_name in extract_slash_skills(text):
            if skill_name in skill_dirs:
                continue
            if skill_name in bundled:
                continue
            if skill_name in false_positives:
                continue
            # Ignorer les `/path/to/file`
            if len(skill_name) <= 2:
                continue
            broken.append((md_file, skill_name))
    return broken


def check_settings_powershell() -> list[str]:
    """Verifie que tous les hooks utilisent PowerShell explicitement."""
    issues: list[str] = []
    settings_path = ROOT / ".claude" / "settings.json"
    if not settings_path.exists():
        return issues

    try:
        cfg = json.loads(read_text(settings_path))
    except json.JSONDecodeError as e:
        issues.append(f"settings.json invalid JSON: {e}")
        return issues

    hooks = cfg.get("hooks", {})
    for event, entries in hooks.items():
        for entry in entries:
            for hook in entry.get("hooks", []):
                if hook.get("type") != "command":
                    continue
                cmd = hook.get("command", "")
                shell = hook.get("shell", "bash")
                # Si le hook utilise bash -c sur Windows, c'est suspect
                if "bash -c" in cmd and shell != "bash":
                    issues.append(
                        f"Hook {event} utilise 'bash -c' sans shell:'bash' (incompatible Windows sans WSL)"
                    )
                if shell not in ("powershell", "bash", "sh", "cmd"):
                    issues.append(f"Hook {event} : shell '{shell}' non standard")
    return issues


def count_skills() -> int:
    skills_dir = ROOT / ".claude" / "skills"
    if not skills_dir.exists():
        return 0
    return sum(1 for d in skills_dir.iterdir() if d.is_dir())


def count_guides() -> int:
    guides_dir = ROOT / ".claude" / "guides"
    if not guides_dir.exists():
        return 0
    return sum(1 for f in guides_dir.iterdir() if f.is_file() and f.suffix == ".md" and f.name != "README.md")


def count_rules() -> int:
    rules_dir = ROOT / ".claude" / "rules"
    if not rules_dir.exists():
        return 0
    return sum(
        1 for f in rules_dir.iterdir()
        if f.is_file() and f.suffix == ".md" and f.name not in ("README.md", "_learned.md")
    )


def check_count_references(skill_count: int, guide_count: int, rule_count: int) -> list[str]:
    """Verifie que les compteurs annonces dans les README/CLAUDE/MEMORY correspondent."""
    issues: list[str] = []

    targets = {
        ROOT / "README.md": [(rf"{skill_count}\s+skills?", f"skills: {skill_count}")],
        ROOT / ".claude" / "memory" / "MEMORY.md": [
            (rf"\*\*{skill_count}\*\*", f"skills: {skill_count}"),
        ],
        ROOT / ".claude" / "skills" / "README.md": [
            (rf"\*\*{skill_count} skills\*\*", f"skills: {skill_count}"),
        ],
    }

    for path, patterns in targets.items():
        if not path.exists():
            continue
        text = read_text(path)
        for pattern, label in patterns:
            if not re.search(pattern, text):
                issues.append(f"{path.relative_to(ROOT)} : compteur attendu {label} non trouve")

    return issues


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    skills_dir = ROOT / ".claude" / "skills"
    skills = list(skills_dir.rglob("SKILL.md")) if skills_dir.exists() else []

    skill_dirs: set[str] = {
        d.name for d in skills_dir.iterdir() if d.is_dir()
    } if skills_dir.exists() else set()

    skill_errors: list[tuple[Path, str]] = []
    for p in sorted(skills):
        t = read_text(p)
        ok, reason = is_valid_skill_frontmatter(t)
        if not ok:
            skill_errors.append((p, reason))

    feature_steps = []
    feature_skill = ROOT / ".claude" / "skills" / "feature" / "SKILL.md"
    if feature_skill.exists():
        for step in ("step-1-explore", "step-2-plan", "step-3-execute", "step-4-verify"):
            sf = ROOT / ".claude" / "skills" / "feature" / "steps" / f"{step}.md"
            feature_steps.append(sf)
    missing_feature_steps = [p for p in feature_steps if not p.exists()]

    important_files = [
        ROOT / "AGENTS.md",
        ROOT / "CLAUDE.md",
        ROOT / "docs" / "workflow-pragmatique.md",
        ROOT / "docs" / "hooks-et-environnement.md",
        ROOT / "docs" / "skills-conventions.md",
        ROOT / "docs" / "integrations" / "assets-pipeline.md",
        ROOT / ".claude" / "rules" / "media-apis.md",
        ROOT / ".claude" / "rules" / "security.md",
        ROOT / ".claude" / "guides" / "README.md",
        ROOT / ".claude" / "agents" / "README.md",
        ROOT / ".claude" / "hooks" / "scripts" / "README.md",
        ROOT / ".claude" / "settings.json",
    ]
    missing_important_files = [p for p in important_files if not p.exists()]

    claude_md = ROOT / "CLAUDE.md"
    missing_from_claude: list[str] = []
    if claude_md.exists():
        t = read_text(claude_md)
        for rel in extract_backticked_paths(t):
            candidate = (ROOT / rel).resolve()
            try:
                candidate.relative_to(ROOT.resolve())
            except Exception:
                continue
            if not candidate.exists():
                missing_from_claude.append(rel)

    rules_readme = ROOT / ".claude" / "rules" / "README.md"
    rules_readme_ok = False
    if rules_readme.exists():
        rt = read_text(rules_readme)
        rules_readme_ok = "media-apis.md" in rt and "Route ou service" in rt

    all_md_files = [p for p in ROOT.rglob("*.md") if "node_modules" not in p.parts]
    broken_links = check_markdown_links(all_md_files)
    claude_lines, claude_over_limit = check_claude_md_line_count()
    agents_warnings = check_agents_md_sync()
    unreferenced_templates = check_templates_referenced()

    skill_count = count_skills()
    guide_count = count_guides()
    rule_count = count_rules()
    count_issues = check_count_references(skill_count, guide_count, rule_count)

    broken_skill_refs = check_skill_references(skill_dirs)
    powershell_issues = check_settings_powershell()

    issues: list[str] = []
    if skill_errors:
        issues.append(f"skills frontmatter issues: {len(skill_errors)}")
    if missing_feature_steps:
        issues.append(f"missing feature steps: {len(missing_feature_steps)}")
    if missing_important_files:
        issues.append(f"missing important files: {len(missing_important_files)}")
    if missing_from_claude:
        issues.append(f"missing paths referenced from CLAUDE.md: {len(missing_from_claude)}")
    if not rules_readme_ok:
        issues.append("rules/README.md missing media-apis structure/activation")
    if broken_links:
        issues.append(f"broken markdown links: {len(broken_links)}")
    if count_issues:
        issues.append(f"count mismatches: {len(count_issues)}")
    if broken_skill_refs:
        issues.append(f"references to non-existent skills: {len(broken_skill_refs)}")
    if powershell_issues:
        issues.append(f"settings.json shell issues: {len(powershell_issues)}")

    warnings: list[str] = []
    if claude_over_limit:
        warnings.append(f"CLAUDE.md is {claude_lines} lines (>120) — context overload risk")
    warnings.extend(agents_warnings)
    for tpl in unreferenced_templates:
        warnings.append(f"unreferenced template: {tpl}")

    print("=== Verify workflow integrity ===")
    print("Root:", ROOT)
    print(f"Skills found: {len(skills)} ({skill_count} folders)")
    print(f"Guides found: {guide_count}")
    print(f"Rules found: {rule_count}")
    print("Skill frontmatter errors:", len(skill_errors))
    print("Missing feature steps:", len(missing_feature_steps))
    print("Missing important files:", len(missing_important_files))
    print("Missing referenced from CLAUDE.md:", len(missing_from_claude))
    print("rules/README.md media-apis check:", "OK" if rules_readme_ok else "KO")
    print(f"CLAUDE.md lines: {claude_lines}", "(OK)" if not claude_over_limit else "(WARNING: >120)")
    print("Broken markdown links:", len(broken_links))
    print("AGENTS.md sync warnings:", len(agents_warnings))
    print("Unreferenced templates:", len(unreferenced_templates))
    print("Count reference issues:", len(count_issues))
    print("Broken skill references:", len(broken_skill_refs))
    print("PowerShell hook issues:", len(powershell_issues))

    if skill_errors:
        for p, reason in skill_errors[:30]:
            print("-", p.relative_to(ROOT), reason)
    if missing_feature_steps:
        for p in missing_feature_steps:
            print("-", p.relative_to(ROOT))
    if missing_important_files:
        for p in missing_important_files:
            print("-", p.relative_to(ROOT))
    if missing_from_claude:
        for rel in missing_from_claude[:30]:
            print("-", rel)
    if broken_links:
        print("\nBroken links:")
        for md_file, link in broken_links[:30]:
            print(f"  {md_file.relative_to(ROOT)} -> {link}")
    if count_issues:
        print("\nCount mismatches:")
        for item in count_issues:
            print(f"  {item}")
    if broken_skill_refs:
        print("\nReferences to non-existent skills:")
        for md_file, skill in broken_skill_refs[:30]:
            print(f"  {md_file.relative_to(ROOT)} -> /{skill}")
    if powershell_issues:
        print("\nPowerShell issues:")
        for item in powershell_issues:
            print(f"  {item}")

    if warnings:
        print("\nWarnings:")
        for w in warnings:
            print(f"  ! {w}")

    if issues:
        print("\nFAIL:", "; ".join(issues))
        raise SystemExit(1)

    print("\nOK: no issues detected.")


if __name__ == "__main__":
    main()

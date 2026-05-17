# Recherche approfondie — workflow IA SaaS & Claude Code (2025–2026)

Synthèse de **sources publiques** (officielles et reconnues) pour compléter `workflow-pragmatique.md`. Les liens pointent vers la doc à jour ; vérifie les URL si une page est déplacée.

---

## 1. Documentation officielle Anthropic (Claude Code)

| Ressource | URL |
|-----------|-----|
| Vue d’ensemble | [docs.anthropic.com — Claude Code overview](https://docs.anthropic.com/en/docs/claude-code/overview) |
| Bonnes pratiques | [docs.anthropic.com — Best practices](https://docs.anthropic.com/en/docs/claude-code/best-practices) |
| Mémoire / `CLAUDE.md` | [docs.anthropic.com — memory](https://docs.anthropic.com/en/memory) |
| Skills | [docs.anthropic.com — skills](https://docs.anthropic.com/en/skills) |
| Hooks | [docs.anthropic.com — hooks](https://docs.anthropic.com/en/hooks) (guide : [hooks-guide](https://docs.anthropic.com/en/hooks-guide)) |
| Sous-agents | [docs.anthropic.com — sub-agents](https://docs.anthropic.com/en/sub-agents) |
| MCP | [docs.anthropic.com — mcp](https://docs.anthropic.com/en/mcp) |
| CLI | [docs.anthropic.com — cli-reference](https://docs.anthropic.com/en/cli-reference) |
| Index machine (`llms.txt`) | [code.claude.com/docs/llms.txt](https://code.claude.com/docs/llms.txt) |

### Points saillants (doc « Best practices »)

- **Fenêtre de contexte** : elle se remplit vite (fichiers lus, sorties terminal, historique). La performance baisse quand elle est pleine — à suivre (ex. status line, réduction des coûts : [costs](https://docs.anthropic.com/en/costs#reduce-token-usage)).
- **Vérification** : donner des tests, critères de succès, captures d’écran attendues — c’est le levier #1 (Claude s’auto-vérifie).
- **Explore → plan → code** : [Plan Mode](https://docs.anthropic.com/en/common-workflows#use-plan-mode-for-safe-code-analysis) pour séparer recherche et exécution ; pour un micro-changement évident, pas besoin de plan lourd.
- **Prompts précis** : fichiers, contraintes, patterns existants dans le repo.
- **`CLAUDE.md`** : court, lisible ; **large** = risque qu’Anthropic décrit : Claude **ignore** des lignes si le fichier est trop chargé. Tableau officiel « inclure / exclure » (commandes non devinables, style *différent* du défaut, quirks du repo ; exclure tutoriels longs, doc API copiée-collée).
- **Import** : syntaxe `@chemin/vers/fichier` dans `CLAUDE.md` pour tirer d’autres fichiers (doc officielle).
- **Permissions** : `/permissions`, sandboxing ; `--dangerously-skip-permissions` seulement dans un contexte contrôlé (avertissement sécurité officiel).
- **MCP** : `claude mcp add` — outils externes (tickets, DB, design…).
- **Hooks** : déterministes vs consignes « conseillées » dans `CLAUDE.md`.
- **Sous-agents** : contexte isolé, outils dédiés (ex. revue sécu).
- **Plugins** : `/plugin` — marketplace.

**Note** : la doc mentionne `/init` pour un **starter** `CLAUDE.md` puis affinage. D’autres auteurs (voir §2) recommandent de **ne pas** se reposer sur une génération automatique sans relecture — les deux idées sont compatibles : *générer un brouillon, puis élaguer et valider à la main*.

---

## 2. `CLAUDE.md` : article HumanLayer (très cité)

| Ressource | URL |
|-----------|-----|
| *Writing a good CLAUDE.md* | [humanlayer.dev/blog/writing-a-good-claude-md](https://www.humanlayer.dev/blog/writing-a-good-claude-md) |
| Contexte (12-factor agents) | [github.com/humanlayer/12-factor-agents](https://github.com/humanlayer/12-factor-agents) (facteur contexte / fenêtre) |

### Idées clés

- **État des LLM** : le modèle ne « connaît » pas le repo sans tokens ; `CLAUDE.md` (ou équivalents type `AGENTS.md` dans d’autres outils) est le vecteur d’onboarding par défaut.
- **Rappel système** : Claude Code injecte un rappel du type *« ce contexte peut ne pas être pertinent — ne réponds que si c’est pertinent »*. Donc du **bruit** dans `CLAUDE.md` peut faire **ignorer** aussi les bonnes règles → **moins d’instructions universelles**, mieux c’est.
- **Recherche (instructions)** : travaux indiquant une **dégradation** de l’adhérence quand le nombre d’instructions augmente ; ordre de grandeur **~150–200** instructions « suivies » selon modèle (en incluant ~50 déjà dans le prompt système Claude Code — ordre de grandeur cité par HumanLayer).
- **Progressive disclosure** : déplacer le détail dans des fichiers séparés (`agent_docs/…`, ou tes `.claude/rules/`, skills, ADR) et **pointer** depuis `CLAUDE.md` plutôt que tout inlined.
- **Pas un linter** : style et formatage → outils déterministes (Biome, ESLint, Prettier, hooks Stop, etc.).
- **Longueur** : consensus informel **moins de 300 lignes**, souvent **beaucoup moins** pour la racine.

---

## 3. Model Context Protocol (MCP)

| Ressource | URL |
|-----------|-----|
| Doc Anthropic | [docs.anthropic.com — mcp](https://docs.anthropic.com/en/mcp) |
| Spécification (évolution) | [modelcontextprotocol.io](https://modelcontextprotocol.io) — la version exacte peut changer ; consulter le site pour la **révision** courante. |
| Écosystème (ex.) | [GitHub — MCP dans Copilot Enterprise](https://docs.github.com/en/enterprise-cloud@latest/copilot/concepts/context/mcp) |

MCP standardise **client ↔ serveurs d’outils** (données, APIs internes). Pour un workflow SaaS : **peu de serveurs**, bien choisis (doc, DB de dev, ticketing), pour éviter explosion de contexte et surface d’attaque.

---

## 4. Autres guides & listes (à croiser)

| Ressource | URL |
|-----------|-----|
| Guide CLAUDE.md (BSWEN, 2026) | [docs.bswen.com — structure CLAUDE.md](https://docs.bswen.com/blog/2026-03-10-how-to-structure-claude-md) |
| Buildcamp — CLAUDE.md | [buildcamp.io — The Ultimate Guide to CLAUDE.md](https://www.buildcamp.io/guides/the-ultimate-guide-to-claudemd) |
| Article Dev.to — prod, MCP, subagents | [dev.to — How to Structure Claude Code for Production](https://dev.to/lizechengnet/how-to-structure-claude-code-for-production-mcp-servers-subagents-and-claudemd-2026-guide-4gjn) |
| Papier (instruction following & volume d’instructions) | [arxiv.org — lien cité par HumanLayer](https://arxiv.org/pdf/2507.11538) |

---

## 5. Alignement avec ce dépôt (claude-saas-blueprint)

| Principe externe | Où c’est dans le projet |
|------------------|-------------------------|
| Moins de contexte global, plus de ciblage | `docs/workflow-pragmatique.md`, section **Niveaux** ; skill `/scope-task` |
| Rules / skills à la demande | `.claude/rules/` ; skills = `.claude/skills/<nom>/SKILL.md` (voir `docs/skills-conventions.md`) |
| Hooks déterministes + OS | `docs/hooks-et-environnement.md`, `.claude/settings.json` |
| Ne pas surcharger `CLAUDE.md` | `CLAUDE.md` racine ; skill `/claude-md-prune` |
| Assets multimédia (fournisseurs, sécurité) | `docs/integrations/*`, rule `media-apis.md`, `/assets-pipeline` |

---

## 6. Prochaines mises à jour

- Revérifier **trimestriellement** les URLs `docs.anthropic.com` (structure des paths `/en/docs/...` peut évoluer).
- Quand tu adoptes **Skills** au format `SKILL.md` avec frontmatter (doc officielle récente), aligner les fichiers de `.claude/skills/` si tu veux la parité avec l’outil.

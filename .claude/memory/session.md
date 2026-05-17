# Session — État de la dernière session

## Date : 2026-05-17

### Cleanup workflow v6 → v7
- **CLAUDE.md** : refondu en overlay Claude Code (~70 lignes), import implicite de `AGENTS.md` qui devient la source unique des conventions communes.
- **AGENTS.md** : refondu, source unique pour tous les outils IA (Claude Code, Cursor, Copilot, Windsurf, Cline, Aider).
- **Skills** : passage de 35 à **31** — fusion de 6 skills UI redondants (`ui-gen`, `ui-premium`, `landing`, `uxui-designer`, `uxui-audit`, `uxui-imagify`) en deux skills clairs : `ui` (modes `gen`, `premium`, `landing`) et `ui-audit` (read-only WCAG/Nielsen/anti-slop).
- **Hooks** : refonte PowerShell-first. Tous les hooks utilisent `"shell": "powershell"` + scripts dans `.claude/hooks/scripts/*.ps1`. Plus de dépendance bash/python3 sur Windows.
- **Subagents vs Guides** : les fichiers `.claude/agents/*` étaient des guides de pattern, pas des subagents. Relocalisés dans `.claude/guides/` ; `.claude/agents/` est maintenant **réservé** pour des vrais subagents custom (frontmatter YAML).
- **Stripe** : `apiVersion` mis à jour vers `2026-03-31`.
- **Validation API** : alignée sur Zod uniquement (Valibot retiré sauf décision projet explicite).
- **Skills morts** corrigés dans la doc : références à des skills inexistants (`profile-setup`, `project-detect`, `mcp-setup`, `coderabbit-setup`, `deploy-vercel-supabase`) remplacées par les skills réels.
- **disable-model-invocation** : règle clarifiée dans `docs/skills-conventions.md` ; appliquée à `quality`, `refactor`, `onboard`.
- **Script verify-workflow-integrity** enrichi : compteurs cohérents, références skills mortes détectées, hooks PowerShell vérifiés, links markdown.

### Fichiers créés
- `.claude/skills/ui/SKILL.md` + `references/{premium-design,landing-patterns,image-pipeline}.md`
- `.claude/skills/ui-audit/SKILL.md`
- `.claude/hooks/scripts/{pre-bash-dangerous,pre-edit-protect,post-edit-format,post-bash-audit,session-start-context,notify-toast}.ps1`
- `.claude/hooks/scripts/README.md`
- `.claude/guides/README.md` + `.claude/agents/README.md`

### Fichiers supprimés
- 6 anciens skills UI redondants

### Fichiers déplacés
- `.claude/agents/*.md` (guides) → `.claude/guides/*.md`

### Prochaine étape
Lancer `/session-start` puis `/saas-init` sur un projet concret pour valider le workflow nettoyé.

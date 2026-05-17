# Veille — outils & plateformes IA (dev, agents, Claude)

**Dernière mise à jour du contenu** : mars 2026 · **Prochaine revue conseillée** : juin 2026 (ou après une annonce majeure type nouveau modèle / MCP).

Ce document complète **[`assets-pipeline.md`](./assets-pipeline.md)** et **`.claude/memory/veille-2026-03.md`**. Il ne remplace pas une veille juridique ou un benchmark de prix : **toujours valider** CGU, tarifs, résidence des données et SLA avant production.

---

## 1. Comment utiliser cette veille

| Objectif | Action |
|----------|--------|
| Choisir des **MCP** pour Claude Code | §3 — privilégier **peu de serveurs** (souvent 0–2) pour limiter contexte et surface d’attaque. |
| Brancher **médias** (SVG, images, voix) | §4 + docs dédiées (`quiver-svg.md`, `pipeline-images.md`, `audio-voice.md`). |
| Étendre **Claude Code** (skills, plugins) | §2 — doc officielle + registres communautaires. |
| Rester à jour | En fin de document : **§8 — processus de mise à jour**. |

---

## 2. Écosystème Claude (Code, plugins, skills)

| Ressource | Lien | Notes |
|-----------|------|--------|
| Claude Code — vue générale | [docs.anthropic.com — Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) | Terminal, IDE, intégrations. |
| MCP dans Claude Code | [docs.anthropic.com — MCP](https://docs.anthropic.com/en/mcp) | Config `claude mcp`, serveurs. |
| Plugins (officiel) | [code.claude.com — plugins reference](https://code.claude.com/docs/en/plugins-reference) | Bundles skills + agents + hooks + MCP. |
| Plugins — aperçu Claude | [claude.com — plugins overview](https://claude.com/docs/plugins/overview) | Vue produit. |
| Plugins — SDK agents | [docs.claude.com — plugins SDK](https://docs.claude.com/en/docs/agent-sdk/plugins) | Intégration programmatique. |
| Registre communautaire (découverte / CLI) | [claude-plugins.dev](https://claude-plugins.dev/) | **Tiers** — vérifier mainteneur et licence avant usage pro. |
| Standard **Agent Skills** (interop outils) | [agentskills.io](https://agentskills.io/) | Aligné avec les dossiers `SKILL.md` de ce repo. |

**Principe** : un plugin ne doit pas dupliquer ce que font déjà **ESLint, tests, CI** — il complète le **contexte** et les **workflows** (revue, design system, etc.).

---

## 3. MCP (Model Context Protocol)

| Ressource | Lien | Notes |
|-----------|------|--------|
| Site & concepts | [modelcontextprotocol.io](https://modelcontextprotocol.io/) | Protocole ouvert (outils, ressources, prompts). |
| Spécification | [spec.modelcontextprotocol.io](https://spec.modelcontextprotocol.io/) | Révisions successives — vérifier la version lue. |
| **Registre officiel** (découverte serveurs) | [modelcontextprotocol.io/registry](https://modelcontextprotocol.io/registry) · [registry.modelcontextprotocol.io](https://registry.modelcontextprotocol.io/) | Métadonnées publiques ; **source de vérité** pour explorer l’écosystème. |
| GitHub — MCP côté Copilot | [GitHub Docs — MCP](https://docs.github.com/en/copilot/concepts/about-mcp) | Intégration IDE (VS Code, JetBrains, etc.). |
| Google — serveurs MCP (GCP, Workspace, etc.) | [github.com/google/mcp](https://github.com/google/mcp) | Catalogue orienté cloud / produits Google. |
| Microsoft — catalogue MCP | [aka.ms/mcp](https://aka.ms/mcp) | Serveurs Microsoft officiels. |

**Rappel** : chaque serveur MCP ajoute des **outils** et du **contexte** — trop de MCP = prompts plus longs et risque de conflits. Configuration via `.claude/mcp/config.json` ou `.vscode/mcp.json` ; recommandé max 2 (Context7 + Supabase MCP).

---

## 4. Génération multimédia & pipelines (SaaS)

Synthèse — le détail opérationnel est dans les fichiers liés :

| Besoin | Doc interne | Fournisseurs / tech (pistes) |
|--------|-------------|--------------------------------|
| **SVG** (génération / vectorisation) | [`quiver-svg.md`](./quiver-svg.md) | [QuiverAI API](https://docs.quiver.ai/api-reference/introduction) |
| **Images** (hero, marketing) | [`pipeline-images.md`](./pipeline-images.md) | [Gemini — images](https://ai.google.dev/gemini-api/docs/image-generation), [fal.ai](https://fal.ai/), [Replicate](https://replicate.com/) |
| **Vidéo** code-first | [`remotion-video.md`](./remotion-video.md) | [Remotion + AI](https://www.remotion.dev/docs/ai/) |
| **Voix / TTS** | [`audio-voice.md`](./audio-voice.md) | [ElevenLabs](https://elevenlabs.io/), TTS cloud classiques |

**Règle transverse** : `.claude/rules/media-apis.md` (clés **serveur uniquement**).

---

## 5. Infra « modèles as a service »

| Plateforme | Lien | Usage typique |
|------------|------|----------------|
| [fal.ai](https://fal.ai/) | Site | APIs modèles, latence, billing unifié (ex. certains modèles image). |
| [Replicate](https://replicate.com/) | Site | Modèles hébergés, scaling horizontal — comparer **prix / cold start**. |
| [Modal](https://modal.com/) | Site | Jobs Python/GPU pour pré/post-traitement autour des modèles. |

Comparer **coût à la requête**, **régions**, et **rétention des données** (RGPD) avant d’embarquer dans le chemin critique utilisateur.

---

## 6. Qualité du code, CI, revue

| Outil / sujet | Lien | Notes |
|---------------|------|--------|
| [CodeRabbit](https://coderabbit.ai/) | Site · [config PR](https://docs.coderabbit.ai/guides/configure-coderabbit) · **[CLI Skills](https://docs.coderabbit.ai/cli/skills)** (revue locale via agent + `coderabbit` CLI) | **Optionnel** — [`coderabbit-optional.md`](./coderabbit-optional.md) (pas de skill packagé). |
| [GitHub Copilot](https://github.com/features/copilot) — Agent / mode agent | GitHub | Complément / alternative aux agents dans l’écosystème Microsoft. |
| Tests & qualité | — | Les **linters et tests déterministes** restent la source de vérité ; l’IA propose, le CI tranche. |

**Mise à jour de stack / libs** (changelogs, breaking changes) : processus dédié [`processus-mise-a-jour-profonde.md`](../processus-mise-a-jour-profonde.md) · skill **`/deep-update`** (pas un simple `npm update`).

---

## 7. Documentation & contexte pour LLM

| Pattern | Lien / référence | Notes |
|---------|------------------|--------|
| Fichiers `llms.txt` / index doc | Ex. [code.claude.com/docs/llms.txt](https://code.claude.com/docs/llms.txt) | Aide les agents à **parcourir** la doc sans tout ingérer. |
| **Context7** | [context7.com](https://context7.com/) | Doc bibliothèques via MCP (souvent cité pour snippets à jour). |
| `CLAUDE.md` / rules scopées | Ce repo : `CLAUDE.md`, `.claude/rules/` | Même philosophie : **peu de contexte global**, beaucoup de **fichiers à la demande**. |

---

## 8. Processus pour mettre à jour cette veille

1. **Trimestriel** : parcourir le [MCP Registry](https://registry.modelcontextprotocol.io/), les release notes **Claude Code** et **Cursor** (ou ton IDE), et retirer les liens morts.
2. **Après une grosse conférence / keynote** (Google I/O, Anthropic, etc.) : ajouter une section « À investiguer » pendant 30 jours, puis fusion ou suppression.
3. **Ne pas** multiplier les lignes sans critère : si un outil ne s’applique pas aux **SaaS B2B** que tu cibles, ne pas l’ajouter.
4. Synchroniser les **décisions** importantes avec `.claude/memory/veille-2026-03.md` (format court).

---

## 9. Limites & éthique (rappel)

- **Hallucinations** : les modèles inventent parfois des APIs — toujours vérifier sur la **doc officielle** du fournisseur.
- **Secrets** : jamais de clés dans le client pour les usages facturés ; voir `media-apis.md`.
- **Données utilisateurs** : flux vers des APIs US / cloud — **DPA** et localisation des données à valider avec le juridique si besoin.

---

## Voir aussi

- [`assets-pipeline.md`](./assets-pipeline.md) — orchestration technique des assets.
- [`.claude/memory/veille-2026-03.md`](../../.claude/memory/veille-2026-03.md) — veille « humaine » / chaînes (Melvynx, etc.).
- [`workflow-pragmatique.md`](../workflow-pragmatique.md) — éviter la surcharge de contexte.

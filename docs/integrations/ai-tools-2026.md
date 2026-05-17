# Outils IA & SaaS — Veille 2026

Outils récents qui ont percé et méritent d'être intégrés dans ce workflow.

## Optimisation tokens

### RTK — Rust Token Killer
- **Rôle** : Proxy CLI qui réduit les tokens de 60-90%
- **Install** : `brew install rtk-ai/tap/rtk && rtk init --global`
- **Doc** : `docs/integrations/rtk-token-optimizer.md`

## Déploiement & Infrastructure

### Vercel (2026)
- **Vercel Agent** : Code review automatique des PR, investigation des anomalies prod
- **Vercel MCP Server** : Intégration directe avec Claude Code pour déployer via MCP
- **Skills.sh** : Écosystème open-source de skills réutilisables pour agents
- **Skill** : `/deploy-check` (audit pré-deploy multi-provider) + `/env-setup` (config Vercel/Supabase)

### Supabase
- **Supabase MCP** : Intégration officielle Claude Code — schema sync, migrations, audit RLS
- **Supabase Connector** : Connecteur officiel Claude (décembre 2025)
- **Install MCP** : `npx supabase mcp` dans `.claude/mcp/config.json`

## Background Jobs & Orchestration

### Trigger.dev v4 ⭐ (recommandé)
- **Rôle** : Queue + workflow + compute engine pour agents IA
- **Pourquoi** : Se positionne comme "meilleure plateforme pour agents IA"
- **Funding** : $3M seed avril 2025
- **Usage SaaS** : emails transactionnels, webhooks, jobs récurrents, pipelines IA
- **Alternative à** : Inngest, BullMQ

### Inngest
- **Rôle** : Orchestration de workflows avec checkpointing et distributed tracing
- **Funding** : $6.1M seed mars 2025
- **Usage** : Workflows complexes avec retry, nested requests

## Bases de données

### Neon (recommandé pour SaaS serverless)
- **Rôle** : PostgreSQL serverless avec branching (comme git pour la DB)
- **Pourquoi** : Scale to zero, branches par PR, compatible Drizzle/Prisma
- **Intégration Supabase** : Alternative ou complément

### Turso (edge)
- **Rôle** : SQLite distribué (<10ms, concurrent writes)
- **Funding** : $8M seed février 2025
- **Usage** : Apps edge, global distribution, faible latence

## Sécurité des dépendances

### Socket.dev ⭐ (recommandé)
- **Rôle** : Analyse comportementale des packages npm (supply chain attacks)
- **Différence vs Snyk** : Détecte les menaces zero-day, pas seulement les CVEs connus
- **Install** : `npm install -g @socket/cli && socket scan`

### Snyk
- **Rôle** : Scan CVEs connus + analyse du code généré par IA
- **Nouveauté 2026** : `snyk_package_health_check` pour assistants IA
- **Usage** : Complémentaire à Socket.dev

## Monitoring & Observabilité

### Sentry (standard)
- SDK Next.js : `@sentry/nextjs`
- Capturer les erreurs serveur + client
- Performance monitoring inclus

### PostHog (analytics + feature flags)
- Open-source, GDPR-friendly
- Feature flags pour déploiements progressifs
- Session recording

## AI Features dans les SaaS

### Vercel AI SDK ⭐
- Intégration Claude via provider Anthropic
- Streaming, tool calls, multi-modal
- AI Gateway : observabilité centralisée des appels LLM
- `npm install ai @ai-sdk/anthropic`

### Anthropic Agent SDK
- Python/TypeScript pour agents programmatiques
- **v2.1+** : subagents avec YAML frontmatter, agent teams, hooks (5 types : command, http, mcp_tool, prompt, agent)
- Custom tools as Python functions
- In-process MCP server support
- Context compaction beta (résumé automatique au seuil de tokens)
- `pip install claude-agent-sdk`

## Modèles Claude (Mars 2026)

| Modèle | Context | Output | Usage |
|--------|---------|--------|-------|
| **Opus 4.6** | 1M (beta) | 128k | Multi-agent, refactoring complexe, thinking adaptatif |
| **Sonnet 4.6** | 200k | 128k | Défaut recommandé, approche Opus, coût moindre |
| **Haiku 4.5** | 200k | 8k | Sous-agents explore, triage, haute fréquence |

- `budget_tokens` **déprécié** → `thinking: adaptive` + `effort: low|medium|high|max`
- Context compaction : beta, résumé auto au seuil, `CLAUDE.md` survit à la compaction

## RSS Feeds Sécurité (à surveiller)

| Feed | Fréquence | URL |
|------|-----------|-----|
| CVEFeed | 15 min | https://cvefeed.io/rssfeed/ |
| CERT-FR | Temps réel | https://www.cert.ssi.gouv.fr/feed/ |
| Zero Day Initiative | Temps réel | https://www.zerodayinitiative.com/rss/ |
| CVEDetails (custom) | Par produit | https://www.cvedetails.com/vulnerability-feeds-form.php |
| CISA KEV | Quotidien | https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json |

## MCP Servers recommandés (max 2)

| MCP | Utilité | Install |
|-----|---------|---------|
| **Context7** | Docs à jour (Next.js, Supabase, Drizzle...) | `npx @context7/mcp` |
| **Supabase MCP** | Opérations DB directement depuis Claude | `npx supabase mcp` |
| Playwright MCP | Tests E2E assistés | `npx @playwright/mcp` |

*Rappel : max 2 MCPs actifs simultanément (10% contexte chacun)*

Les MCPs peuvent être **scopés à un subagent** via le frontmatter YAML dans `.claude/agents/*.md` :

```yaml
mcpServers:
  supabase:
    command: npx
    args: ["supabase", "mcp"]
```

30+ MCP servers publics disponibles dans l'écosystème. Catalogue : `modelcontextprotocol.io/servers`

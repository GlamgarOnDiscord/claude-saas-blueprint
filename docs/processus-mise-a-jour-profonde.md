# Processus — mise à jour profonde (« deep update »)

Tu t’es probablement exprimé correctement : l’idée est qu’**avant** de modifier du code pour une lib, un framework ou une API externe, l’agent **recherche d’abord** ce qui a changé depuis ta baseline (version actuelle, date, comportement attendu), puis applique une **migration propre** (clean code, pas de rustines).

Ce processus est **distinct** de `/deps` (audit rapide `outdated` / audit sécu) : ici on vise une **compréhension large** des changements **breaking**, dépréciations et bonnes pratiques **récentes**.

## Quand l’utiliser

- Montée de version **majeure** (ex. Next 14 → 15, Prisma 5 → 6).
- API externe qui **déprécie** un endpoint ou change le modèle de facturation.
- Sécurité : CVE qui exige une version minimale avec **changements d’API**.
- Tu reprends un repo après **6+ mois** sans toucher une brique critique.

## Quand ne pas l’utiliser

- Bump **patch** sans changelog notable → `/deps` ou PR minimale.
- Tu ne sais pas encore **quoi** mettre à jour → cadrer le scope d’abord (`/scope-task`).

## Étapes (ordre recommandé)

### 1. Cadrer **X**

- Nom précis : ex. `next`, `@tanstack/react-query`, `stripe` SDK, API REST interne `v1 → v2`.
- Périmètre : **un** sujet principal par session (sinon perte de focus).

### 2. Établir la **baseline** (état actuel)

- Lire `package.json` / lockfile / version runtime déployée.
- Noter la **version cible** souhaitée (ou « dernière LTS »).
- Si pertinent : dernière fois que le projet a été migré → `.claude/memory/stack.md` ou `decisions.md`.

### 3. Recherche **profonde** (obligatoire avant gros diffs)

L’agent doit consulter des sources **officielles** en priorité :

| Source | Exemple |
|--------|---------|
| Changelog / release notes | GitHub **Releases**, blog du framework |
| Guide de migration | `https://…/docs/migration` |
| Dépréciations | issue « breaking changes » pinned |
| Sécurité | GHSA, advisory npm |

Outils : **WebSearch**, **WebFetch** sur les URLs officielles, lecture des fichiers du repo impactés.

**Sortie attendue** (court document ou section de plan) :

- Liste des **breaking changes** qui t’concernent (pas tout le changelog).
- Fichiers / modules du repo **touchés**.
- Ordre de migration (ex. types d’abord, puis runtime).

### 4. Plan puis exécution **clean**

- Petits commits logiques ou une PR par étape si gros chantier.
- Éviter les `any` et les `@ts-expect-error` sauf transition documentée.
- Mettre à jour **tests** et **types** en même temps que le runtime.

### 5. Vérification

- `tsc --noEmit`, tests blast radius, smoke manuel sur les flux critiques.
- CI verte avant merge.

### 6. Mémoire projet

- Mettre à jour `.claude/memory/stack.md` (versions).
- Si décision durable : une ligne dans `decisions.md` ou ADR.

## Skill associé

**`/deep-update`** — charge ce document et force la séquence *baseline → recherche → plan → code*.

## Relation avec d’autres skills

| Skill | Rôle |
|-------|------|
| `/deps` | Scan large des paquets, audit, outdated — **pas** migration guidée changelog par changelog. |
| `/migrate` | Peut chevaucher ; si la migration est **documentée** ailleurs, préférer `/deep-update` pour la **phase recherche**. |
| `/apex` | Utile pour structurer **Analyze → Plan → Execute → Examine** sur ce chantier. |

---

Voir aussi : [`workflow-pragmatique.md`](./workflow-pragmatique.md), [`recherche-sources-2026.md`](./recherche-sources-2026.md).

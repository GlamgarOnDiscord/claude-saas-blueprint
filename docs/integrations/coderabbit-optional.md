# CodeRabbit — revue PR IA (optionnel)

**Rien dans ce dépôt n’impose CodeRabbit.** Active-le **uniquement** si tu veux des revues automatisées sur les PR (GitHub / GitLab / Azure DevOps selon l’offre).

## À quoi ça sert

- Commentaires et suggestions sur les **pull requests** (sécurité, style, cohérence).
- Complète — ne remplace pas — **CI, tests, linters** et review humaine.

---

## Voie A — App + `.coderabbit.yaml` (revue sur PR)

1. Créer un compte / installer l’app **CodeRabbit** sur ton **org ou repo** (voir [Getting started](https://docs.coderabbit.ai/getting-started/configure-coderabbit)).
2. Ajouter un fichier **`.coderabbit.yaml`** à la **racine du dépôt applicatif** (pas obligatoirement ce template workflow).
3. Ajuster profil de revue, langue, branches ignorées, etc. — [Configuration](https://docs.coderabbit.ai/guides/configure-coderabbit) · [YAML / schéma](https://docs.coderabbit.ai/configuration/yaml-validator).

Exemple minimal (indicatif — vérifier la doc à jour pour les clés exactes) :

```yaml
# yaml-language-server: $schema=https://coderabbit.ai/integrations/schema.v2.json
language: "fr-FR"
reviews:
  profile: "assertive"
  auto_review:
    enabled: true
    drafts: false
```

---

## Voie B — CLI + **Skills** agent (revue locale depuis l’IDE / Claude Code)

Pour déclencher une analyse des **changements locaux** via le **CodeRabbit CLI** et des skills au format `SKILL.md` (standard [Agent Skills](https://agentskills.io/)), voir la doc officielle :

**[CodeRabbit Skills — documentation](https://docs.coderabbit.ai/cli/skills)**

### Résumé

1. Installer et authentifier le CLI ([instructions dans la doc Skills](https://docs.coderabbit.ai/cli/skills)) :
   - `curl -fsSL https://cli.coderabbit.ai/install.sh | sh`
   - `coderabbit auth login`
2. Installer le paquet de skills (ex. pour Claude Code) :
   - `npx skills add coderabbitai/skills -a claude-code`
   - ou sans `-a` pour tous les agents détectés ; `-g` pour installation utilisateur.
3. Skills fournis (dont `code-review`, `autofix`) : déclenchables en langage naturel dans l’agent ; le skill invoque le CLI (`coderabbit` avec flags documentés).

**Skills vs PR GitHub** : les skills complètent la voie A — revue **locale** / boucle implement → review → fix, sans remplacer la config `.yaml` sur le dépôt distant si tu l’utilises déjà.

Dépôt open-source des skills : [github.com/coderabbitai/skills](https://github.com/coderabbitai/skills).

Intégrations agent détaillées : [CLI — index](https://docs.coderabbit.ai/cli/index) (Claude Code, Cursor, etc.).

---

## Lien avec l’agent IA local

- **Voie A** : CodeRabbit sur le **remote** (PR).
- **Voie B** : CodeRabbit **CLI** dans le flux de travail **local** (branche courante, avant push).
- Les deux peuvent coexister.

## Skill associé (ce repo)

Aucun skill packagé pour CodeRabbit. Pour automatiser ta config, utilise `meta-prompt skill coderabbit-setup [description]` qui te génèrera un skill custom à partir des étapes ci-dessus.

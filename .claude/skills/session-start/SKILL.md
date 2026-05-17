---
name: session-start
description: "Démarre une session proprement : lire la mémoire, router vers le bon skill, et si profil vide — interview rapide pour remplir user-profile.md."
disable-model-invocation: true
---

# Session Start (First Contact)

À utiliser au **début d'une session** ou quand l'utilisateur dit « par où commencer ».

## 1. Lire l'état

- `.claude/memory/user-profile.md`
- `.claude/memory/session.md`
- Si présent : `.claude/memory/stack.md`, `.claude/memory/project-scan.md`

## 2. Router

| Situation | Action |
|-----------|--------|
| Profil vide / champs "Non défini" | → Étape 3 : interview profil |
| Repo inconnu / jamais scanné | Proposer `/onboard` |
| Dépôt vide ou sans stack | Proposer `/saas-init` |
| Tout est OK | Résumer stack + 1 priorité utilisateur |

## 3. Interview profil (si profil incomplet)

Poser ces questions via AskUserQuestion — **une à la fois** :

1. **Package manager** préféré ? `pnpm` | `bun` | `npm`
2. **Stack frontend** habituelle ? `Next.js` | `Remix` | `Nuxt` | autre
3. **DB** préférée ? `Supabase` | `Neon + Drizzle` | `Prisma + PostgreSQL` | autre
4. **Verbosité des réponses** ? `concise` | `normal` | `détaillé`
5. **Demander avant d'agir** ? `toujours` | `si risqué` | `jamais`

Après les réponses → mettre à jour `.claude/memory/user-profile.md` avec les valeurs réelles.

## 4. Sortie attendue

- **Résumé en ≤8 lignes** : qui (profil), quoi (projet), où (stack), prochaine action unique.
- **Une** prochaine étape claire — pas une liste de skills.

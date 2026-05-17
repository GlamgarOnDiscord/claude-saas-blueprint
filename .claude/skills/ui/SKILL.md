---
name: ui
description: "Generation d'interfaces SaaS — basic, premium dark-mode, ou landing page complete. Choisir le mode selon le besoin."
argument-hint: "- `mode` : gen | premium | landing - `target` : description de la page/composant"
disable-model-invocation: true
---

## Modes

| Mode | Quand l'utiliser | Output |
|------|------------------|--------|
| `gen` | Composant ou page interne, design system existant | Composants composables, mobile-first, shadcn/ui |
| `premium` | Marketing site, dashboard premium, dark-mode-first | Vercel/Linear/Stripe aesthetic, motion, bento grids |
| `landing` | Landing page complete avec conversion (waitlist, signup) | Hero → Social proof → Features → Pricing → FAQ → CTA |

> **UI 3D / WebGL** : stack recommandee R3F + drei + GSAP ScrollTrigger + Lenis. Voir `platforms/web-app.md` et `docs/integrations/assets-pipeline.md` (section scroll 3D). Reserve aux pages qui en ont reellement besoin.

---

## `/ui gen [target]` — Generation classique

### 1. Comprendre le besoin
- Identifier le type : dashboard, formulaire, settings, profil, feature page
- Verifier les composants UI deja installes (`components/ui/`)
- Lire `rules/ui-components.md` AVANT toute modification

### 2. Design system check
- Composants shadcn/ui presents → privilegier
- Si manquant → utiliser l'outil `21st_magic_component_builder` (si MCP configure) ou installer le composant officiel
- Si inspiration necessaire → `21st_magic_component_inspiration`

### 3. Generation
Principes :
- **Mobile-first** — commencer par 375px, etendre vers desktop
- **Server Components** par defaut. `"use client"` uniquement si interactivite (hooks, animations, listeners)
- **Composition** — assembler des composants petits, pas un monolithe
- **Accessibilite** — labels, aria, focus management, contraste WCAG AA minimum
- **Loading states** — Skeleton screens, jamais de spinner
- **Max 150 lignes** par composant — split sinon

Structure type d'une page :
```
page.tsx              → Server Component, data fetching
├── page-header       → Titre, breadcrumb, actions
├── page-content      → Contenu principal (sections)
└── page-footer       → Actions secondaires (optionnel)
```

### 4. Validation
- Screenshot ou preview si possible
- Responsivite : sm (375px) · md (768px) · lg (1280px+)
- Tous les etats couverts : loading, empty, error, success
- `tsc --noEmit`

---

## `/ui premium [target]` — Mode premium dark-mode

> Charger `references/premium-design.md` pour les details (couleurs, typographie, anti-patterns, sections, composants).

### Principes-clefs
- Dark-mode first : `#09090b` (zinc-950), jamais `#000000` pur
- Une seule couleur d'accent (violet-500 ou blue-500)
- Typographie : Geist, Satoshi, DM Sans — **jamais Inter** sur les dashboards
- Layout asymetrique par defaut (variance >= 5)
- Animations : transform / opacity uniquement, 0.3-0.6s ease-out
- Composition avant decoration — pas de glassmorphism lourd ni de neon

### Anti-patterns interdits
- Hero centre quand variance > 4
- 3 cards egales en ligne (preferer asymetrie ou bento)
- Web3 / cyberpunk / neons satures
- Spinner au lieu de Skeleton
- Inter / Roboto / Arial / Space Grotesk
- Numeros ronds (`50%`, `1000+`) — toujours organique (`47.2%`, `2 847`)

### Workflow
1. Lire `references/premium-design.md` (constraints, sections, composants)
2. Calibrer les dials selon le type :
   - Landing marketing : `variance=8 motion=6 density=4`
   - Dashboard interne : `variance=4 motion=4 density=8`
3. Generer en respectant la structure de conversion
4. Self-check obligatoire :
   - [ ] Aucune section transposable telle quelle dans un autre projet
   - [ ] Hero a un point focal dominant et un CTA primaire specifique
   - [ ] Sections adjacentes utilisent des grammaires de layout differentes
   - [ ] Police choisie n'est ni Inter, Roboto, Arial, ni Space Grotesk
   - [ ] Au moins une decision de design surprendrait un designer attendant "du AI generique"
5. Si 2+ checks echouent → corriger avant de livrer

---

## `/ui landing [target]` — Landing page complete

### Phase 1 — Brief (AskUserQuestion)
1. Nom + tagline
2. Proposition de valeur (probleme resolu)
3. Cible (devs, PME, B2C)
4. CTA principal : `waitlist | signup | buy | demo`

### Phase 2 — Structure de conversion (ordre fixe)
```
1. Hero          — H1 + sous-titre + CTA + visuel
2. Social proof  — logos / "X+ utilisateurs" / score
3. Probleme      — 3 pain points (icone + texte court)
4. Solution      — 3 benefices, pas features techniques
5. Features      — details + visuels ou code snippets si B2B dev
6. Temoignages   — 2-3 quotes (nom, avatar, titre)
7. Pricing       — 3 plans max, plan recommande mis en avant
8. FAQ           — 5-6 questions, accordeon
9. CTA Final     — rappel tagline + bouton + social proof chiffre
```

### Phase 3 — Implementation

Structure fichiers :
```
app/(marketing)/
├── page.tsx
└── _components/
    ├── hero.tsx · social-proof.tsx · problem.tsx
    ├── features.tsx · testimonials.tsx · pricing.tsx
    ├── faq.tsx · cta-final.tsx
```

Hero avec waitlist (exemple-pattern, voir `references/landing-patterns.md` pour code complet) :
```tsx
'use client'
// ...form submit → POST /api/waitlist + tracking PostHog
```

Route waitlist :
```ts
// app/api/waitlist/route.ts — Zod validation + Resend confirmation
```

### Phase 4 — SEO et perf
- Meta title + description + OpenGraph (`og:image` 1200x630)
- Sitemap + robots.txt
- Lighthouse > 90 (perf, a11y, SEO, best practices)
- CTA visible above the fold sur 375px
- `loading="lazy"` sur les images hors viewport, `width`/`height` toujours specifies

---

## Quand utiliser quoi ?

| Question | Mode |
|----------|------|
| "Ajoute une page settings" | `gen` |
| "Refais le dashboard avec un look Linear" | `premium` |
| "Fais une landing pour mon SaaS" | `landing` |
| "Audit accessibilite de cette page" | `/ui-audit` |
| "Genere des images Gemini pour la landing" | utiliser `references/image-pipeline.md` du mode `landing` |

## References

- `references/premium-design.md` — design tokens, sections, composants premium
- `references/landing-patterns.md` — code complet hero/pricing/FAQ/waitlist
- `rules/ui-components.md` — regles obligatoires (loading states, max lignes, etc.)
- `platforms/web-app.md` — stack web et patterns
- `docs/integrations/assets-pipeline.md` — generation d'images, SVG, scroll 3D

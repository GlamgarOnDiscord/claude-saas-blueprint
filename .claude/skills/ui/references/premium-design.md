# Premium Design — Reference complete

## Couleurs dark-mode-first
```
Fond principal  : #09090b (zinc-950) — jamais #000000 pur
Fond cards      : zinc-900 / zinc-800
Borders         : border-white/5 a border-white/10
Text principal  : text-white
Text secondaire : text-zinc-400
Text muted      : text-zinc-500
Accent          : violet-500 / blue-500 / emerald-500 (1 seul par produit)
```

## Typographie
```
Display/Titres  : Geist, Satoshi, Cabinet Grotesk, Bricolage Grotesque
Body            : DM Sans (14-16px), Geist Sans
Data/Mono       : Geist Mono, JetBrains Mono
```
**Interdit** : Inter, Roboto, Arial, Space Grotesk, serif, emojis dans le code/copy.

## Layout standard
```tsx
// Container
<div className="max-w-7xl mx-auto px-6">

// Sections
<section className="py-24 md:py-32">

// Grilles
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

// Hauteur viewport (jamais h-screen)
<div className="min-h-[100dvh]">
```

## Animations — regles strictes
- Uniquement `transform` et `opacity` (pas `width`/`height`/`top`)
- Duree : 0.3-0.6s, easing `ease-out` ou `ease-in-out`
- Loops perpetuelles → composant isole avec `React.memo`
- **Framer Motion** uniquement pour layout animations, drag, stagger, physics
- CSS transitions natives pour hover simples (suffisant 80% du temps)
- `prefers-reduced-motion` toujours respecte

## Anti-patterns — interdits

```
- Web3 / cyberpunk / neons satures
- Grands degrades de fond (gradient sur tout le hero)
- Glassmorphism lourd (backdrop-blur sur tout)
- Glows colores intenses
- Hero text centre quand DESIGN_VARIANCE > 4
- Layouts Bootstrap-like (rows/cols egaux partout)
- Images non compressees
- style={{}} inline sauf valeurs dynamiques
- Spinner de chargement (utiliser Skeleton)
- Inter/Roboto/Arial/Space Grotesk
- Numeros ronds (50%, 1000+) — preferer 47.2%, 2 847
- 3 cards egales en ligne — preferer asymetrie ou bento
```

## Structure de fichiers (obligatoire)

```
app/(marketing)/_components/    ← pages publiques
app/(app)/_components/          ← pages authentifiees
components/ui/                  ← shadcn + primitives
components/blocks/              ← sections reutilisables (hero, pricing, faq)
```

Regle : 1 composant = 1 fichier, max 150 lignes. Split sinon.

## Sections landing (ordre de conversion)

### Header / Nav (sticky glass subtil)
```tsx
<header className="sticky top-0 z-50 border-b border-white/5 bg-zinc-950/80 backdrop-blur-sm">
  {/* Logo + nav + CTA */}
</header>
```

### Hero (left-aligned, jamais centre)
```tsx
<section className="min-h-[100dvh] flex flex-col justify-center pt-20">
  {/* Badge */}
  <div className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs text-zinc-400 mb-6">
    <span className="h-1.5 w-1.5 rounded-full bg-green-400 animate-pulse" />
    Nouveau — v2.0 disponible
  </div>

  {/* Titre XXL */}
  <h1 className="text-6xl md:text-8xl font-bold tracking-tight text-white max-w-4xl">
    Construis ton SaaS{' '}
    <span className="text-violet-400">10x plus vite</span>
  </h1>

  {/* 2 CTAs */}
  <div className="flex gap-3 mt-8">
    <Button size="lg">Commencer gratuitement →</Button>
    <Button variant="outline" size="lg">Voir la demo</Button>
  </div>

  {/* Social proof organique */}
  <p className="text-zinc-500 text-sm mt-6">
    Rejoint par <span className="text-white">2 847</span> developpeurs
    · Note moyenne <span className="text-white">4.8/5</span>
  </p>
</section>
```

### Social proof
- Logos clients en `grayscale opacity-40 hover:opacity-100`
- Stats organiques : `47.2%` jamais `50%`, `2 847` jamais `3 000`
- Testimonials : avatar reel + nom + titre + quote courte (< 2 lignes)

### Features — bento grid
```tsx
<div className="grid grid-cols-1 md:grid-cols-3 gap-4">
  {/* Card grande — span 2 colonnes */}
  <div className="col-span-2 rounded-2xl border border-white/10 bg-zinc-900 p-6 group hover:border-violet-500/30 transition-colors">
    <div className="mb-4 text-violet-400">{/* SVG icon */}</div>
    <h3 className="text-lg font-semibold text-white mb-2">Feature principale</h3>
    <p className="text-zinc-400 text-sm">Description concise — benefice, pas feature.</p>
  </div>
  {/* Card petite */}
</div>
```

### Pricing
```tsx
{/* Plan recommande : ring + badge flottant */}
<div className="relative rounded-2xl border-2 border-violet-500 bg-zinc-900 p-8">
  <span className="absolute -top-4 left-1/2 -translate-x-1/2 rounded-full bg-violet-500 px-4 py-1 text-xs font-semibold text-white">
    Le plus populaire
  </span>
</div>
```

### FAQ — accordeon
```tsx
<AnimatePresence>
  {open && (
    <motion.div
      initial={{ height: 0, opacity: 0 }}
      animate={{ height: 'auto', opacity: 1 }}
      exit={{ height: 0, opacity: 0 }}
      transition={{ duration: 0.3, ease: 'easeOut' }}
    >
      {answer}
    </motion.div>
  )}
</AnimatePresence>
```

## Composants premium

### Shimmer button
```tsx
<button className="relative inline-flex overflow-hidden rounded-lg border border-white/10 bg-zinc-900 px-6 py-3 text-sm font-medium text-white group">
  <span className="absolute inset-0 -translate-x-full animate-[shimmer_2s_infinite] bg-gradient-to-r from-transparent via-white/10 to-transparent group-hover:translate-x-full transition-transform" />
  {children}
</button>
```

### Liquid glass card (subtil)
```tsx
<div className="rounded-2xl border border-white/5 bg-white/[0.02] backdrop-blur-sm p-6">
  ...
</div>
```

## Etats SaaS obligatoires

```tsx
// Loading — Skeleton, jamais spinner
<Skeleton className="h-8 w-48 bg-zinc-800" />

// Empty
<div className="flex flex-col items-center gap-3 py-16 text-zinc-500">
  <Icon className="h-8 w-8 opacity-40" />
  <p>Aucun element pour l'instant</p>
  <Button variant="outline" size="sm">Creer le premier</Button>
</div>

// Error
<div className="rounded-lg border border-red-500/20 bg-red-500/5 p-4 text-red-400 text-sm">
  {message}
</div>
```

## Checklist avant livraison

- [ ] `tsc --noEmit` zero erreur
- [ ] Responsive 375px / 768px / 1440px
- [ ] Tous etats : loading / empty / error / success
- [ ] Aucun `style={{}}` sauf valeurs dynamiques
- [ ] Animations sur transform/opacity uniquement
- [ ] Skeleton partout au lieu de spinner
- [ ] Images avec alt + width + height (pas de CLS)
- [ ] Lighthouse perf > 90
- [ ] WCAG AA minimum (viser AAA)

## Style auto-router

| Brief contient… | Mood | Variance | Motion | Density |
|-----------------|------|----------|--------|---------|
| B2B / dashboards / data | `dashboard-pro` | 4 | 4 | 8 |
| dark / Linear / Vercel | `dark-saas` | 8 | 6 | 4 |
| editorial / portfolio | `editorial-premium` | 6 | 5 | 3 |
| warm / human / startup | `warm-startup` | 5 | 5 | 4 |
| produit / hardware / launch | `product-cinematic` | 7 | 8 | 3 |
| swiss / institutional / grid | `swiss-precision` | 5 | 3 | 5 |
| consumer / lifestyle | `soft-consumer` | 4 | 6 | 4 |

## Quick decision shortcuts

- **"premium"** → restraint et whitespace > decoration
- **"bold"** → contraste structurel > chaos
- **"modern"** → strip generic conventions first
- **"minimal"** → enlever les composants faibles avant de tout retrecir
- **"clean"** → augmenter le negative space, reduire la variete couleurs
- **"editorial"** → ameliorer le pacing des sections > ajouter du serif partout
- **"playful"** → garder la composition disciplinee
- **"futuristic"** → eviter les tropes sci-fi (neon glows, scanlines)

## Failure mode recovery

- **Looks like a template** → casser le rythme repetitif, varier les layouts
- **Looks generic** → renforcer typographie hierarchy et hero composition d'abord
- **Looks cheap** → enlever neon, reduire saturation, remplacer rounded cards par bordered
- **Looks crowded** → enlever le chrome avant de retrecir les fonts
- **Hero ne lit pas** → un point focal dominant + un support + whitespace
- **Sections identiques** → varier carded vs open, image-left vs image-right
- **CTA faible** → dire exactement ce qui se passe ("Open the dashboard" vs "Get started")

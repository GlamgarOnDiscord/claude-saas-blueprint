# Platform: Web Application

## Stacks Recommandées (2026)

### Option A — Next.js Full-Stack (Recommandé pour SaaS)
- **Framework**: Next.js 15+ (App Router)
- **Runtime**: Node.js 22+ ou Bun
- **UI**: React 19 + Tailwind CSS 4 + shadcn/ui
- **State**: Zustand ou Jotai (pas Redux)
- **Forms**: React Hook Form + Zod
- **DB**: PostgreSQL + Drizzle ORM
- **Auth**: Auth.js v5 ou Clerk
- **Paiements**: Stripe
- **Email**: Resend + React Email
- **Deploy**: Vercel
- **Tests**: Vitest + Playwright

### Option B — Remix/React Router 7
- Pour apps avec beaucoup de formulaires et progressive enhancement

### Option C — Nuxt 4
- Si l'utilisateur préfère Vue.js

### Option D — SvelteKit 2
- Pour performance maximale et bundle minimal

## Conventions Web
- SSR par défaut, CSR uniquement quand nécessaire
- Server Components pour le data fetching
- Streaming + Suspense pour le loading
- Optimistic UI pour les mutations
- ISR pour le contenu semi-statique
- Edge Runtime pour les endpoints légers

## Structure Next.js Recommandée
```
app/
├── (auth)/              # Groupe de routes auth
│   ├── login/
│   └── register/
├── (dashboard)/         # Groupe de routes app
│   ├── layout.tsx       # Sidebar + nav
│   ├── page.tsx         # Dashboard home
│   └── [feature]/       # Feature pages
├── api/                 # API routes
│   └── [resource]/
├── layout.tsx           # Root layout
└── page.tsx             # Landing page
src/
├── core/                # Logique métier
├── adapters/            # Implémentations
├── shared/              # Types, utils
├── components/          # UI components
│   ├── ui/              # Primitives (shadcn)
│   └── features/        # Components métier
├── hooks/               # React hooks custom
└── lib/                 # Configs (db, auth, etc.)
```

## Checklist Web App
- [ ] Responsive (mobile-first)
- [ ] SEO meta tags
- [ ] OpenGraph images
- [ ] Favicon + PWA manifest
- [ ] Error boundaries
- [ ] Loading states (skeletons)
- [ ] 404 / 500 pages custom
- [ ] Analytics (Posthog / Vercel Analytics)
- [ ] Rate limiting sur API
- [ ] CORS configuré
- [ ] CSP headers

## Assets & médias (génération IA)
- Vue d’ensemble : **`docs/integrations/assets-pipeline.md`** · règle **`.claude/rules/media-apis.md`** (clés serveur).
- Détail par fournisseur : **`docs/integrations/quiver-svg.md`**, **`pipeline-images.md`**, **`remotion-video.md`**, **`audio-voice.md`** (ElevenLabs).
- **Scroll 3D « premium »** : `@react-three/fiber`, `@react-three/drei`, `three`, **GSAP** `ScrollTrigger`, **Lenis** (scroll inertiel). Pas d’API clé côté navigateur pour la 3D — uniquement assets et code. Ex. tutoriel [Codrops + GSAP 2025](https://tympanus.net/codrops/2025/11/19/how-to-build-cinematic-3d-scroll-experiences-with-gsap/).
- Skill **`/ui`** (modes `landing` et `premium`) référence cette stack pour les cas avancés.
- Veille outils : **`docs/integrations/ai-tools-veille-2026.md`**

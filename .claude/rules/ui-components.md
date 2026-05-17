# Rules: UI Components

## Obligatoire
- Utiliser les composants shadcn/ui existants avant d'en créer de nouveaux
- Toujours ajouter des loading states (Skeleton, pas spinner)
- Toujours ajouter des error states avec message utilisateur clair
- Toujours rendre responsive (mobile-first, tester sm/md/lg)
- Server Components par défaut, "use client" uniquement si interactivité
- Formulaires avec React Hook Form + Zod, jamais de state manuel

## Interdit
- Ne PAS créer de composants > 150 lignes — split en sous-composants
- Ne PAS hardcoder des couleurs — utiliser les CSS variables du thème
- Ne PAS utiliser `style={{}}` inline — utiliser Tailwind
- Ne PAS oublier les attributs d'accessibilité (labels, aria)

## Learned
<!-- Règles ajoutées automatiquement par l'agent -->

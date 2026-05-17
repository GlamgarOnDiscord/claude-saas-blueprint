# Platform: Mobile Application

## Stacks Recommandées (2026)

### Option A — React Native + Expo (Recommandé)
- **Framework**: Expo SDK 52+ (Managed Workflow)
- **Navigation**: Expo Router (file-based)
- **UI**: Tamagui ou NativeWind (Tailwind pour RN)
- **State**: Zustand + React Query / TanStack Query
- **Storage**: Expo SecureStore + MMKV
- **Auth**: Clerk / Supabase Auth / Firebase Auth
- **Push**: Expo Notifications
- **OTA Updates**: Expo Updates / EAS Update
- **Build**: EAS Build
- **Tests**: Jest + Detox (E2E)

### Option B — Flutter
- Si l'utilisateur préfère Dart ou besoin de performances natives pures

### Option C — SwiftUI + Kotlin (Natif pur)
- Si performance critique ou intégrations système profondes

## Conventions Mobile
- Navigation Stack par défaut (pas de tabs sauf si justifié)
- Offline-first : cache local avec sync en arrière-plan
- Animations natives (Reanimated 3+ pour RN)
- Deep linking configuré dès le début
- Biometric auth quand disponible
- Respecter les guidelines iOS HIG et Material 3

## Structure Expo Router Recommandée
```
app/
├── (auth)/
│   ├── login.tsx
│   └── register.tsx
├── (tabs)/
│   ├── _layout.tsx      # Tab navigator
│   ├── home.tsx
│   ├── profile.tsx
│   └── settings.tsx
├── [feature]/
│   ├── index.tsx
│   └── [id].tsx
├── _layout.tsx           # Root layout
└── +not-found.tsx
src/
├── core/                 # Logique métier (partageable avec web)
├── adapters/
│   ├── api/              # API client
│   ├── storage/          # Persistent storage
│   └── notifications/    # Push notifications
├── components/
│   ├── ui/               # Primitives
│   └── features/         # Components métier
├── hooks/
└── lib/
```

## Checklist Mobile
- [ ] Splash screen configuré
- [ ] App icon toutes tailles
- [ ] Deep linking
- [ ] Push notifications
- [ ] Offline mode basique
- [ ] Biometric auth (optionnel)
- [ ] Rate limiting API client-side
- [ ] Error boundaries
- [ ] Crash reporting (Sentry)
- [ ] Analytics (Posthog / Amplitude)
- [ ] Store listing (screenshots, description)
- [ ] Privacy policy URL

---
name: assets-pipeline
description: "Génère et intègre des assets multimédia dans un SaaS : images IA (Gemini), SVG (Quiver), vidéo (Remotion), audio (ElevenLabs), scroll 3D. Clés serveur, stockage objet, charte."
disable-model-invocation: true
---

## Quand utiliser ce skill
- Ajouter une génération d'image, SVG, vidéo ou audio dans le produit
- Setup scroll 3D / WebGL sur landing ou app
- Aligner landing, marketing et UI sur une même charte visuelle
- Avant d'ajouter des variables d'environnement liées aux APIs d'assets

## Règle absolue (voir `rules/media-apis.md`)
- Appels API assets = **server-side uniquement** (route API, worker, cron)
- Jamais `NEXT_PUBLIC_*` pour `QUIVERAI_*`, `GOOGLE_API_KEY`, `ELEVENLABS_*`
- Sortie → stockage objet (Supabase Storage / S3) + URL signée ou CDN
- Lier chaque asset généré à `organizationId` / `userId` en DB (multi-tenant)

---

## Images IA — Gemini

```typescript
// app/api/generate-image/route.ts (server-side uniquement)
import { GoogleGenerativeAI } from '@google/generative-ai'

const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY!)

export async function POST(req: Request) {
  const { prompt } = await req.json()
  const model = genAI.getGenerativeModel({ model: 'gemini-2.0-flash-exp-image-generation' })

  const result = await model.generateContent(prompt)
  const imageData = result.response.candidates?.[0]?.content.parts
    .find(p => p.inlineData)?.inlineData

  // Uploader vers Supabase Storage
  const { data } = await supabase.storage
    .from('assets')
    .upload(`generated/${Date.now()}.png`, Buffer.from(imageData!.data, 'base64'), {
      contentType: 'image/png',
    })

  return NextResponse.json({ url: data?.path })
}
```

Docs : https://ai.google.dev/gemini-api/docs/image-generation

---

## SVG — Quiver AI

```typescript
// app/api/generate-svg/route.ts
const res = await fetch('https://api.quiver.ai/v1/svg', {
  method: 'POST',
  headers: { Authorization: `Bearer ${process.env.QUIVERAI_API_KEY}` },
  body: JSON.stringify({ prompt, style: 'minimal', format: 'svg' }),
})
const { svg } = await res.json()
// Stocker en DB ou Supabase Storage
```

Docs : https://docs.quiver.ai/api-reference/introduction

---

## Vidéo — Remotion

```bash
pnpm create video@latest
```

```typescript
// remotion/MyVideo.tsx
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion'

export const MyVideo = () => {
  const frame = useCurrentFrame()
  const opacity = interpolate(frame, [0, 30], [0, 1])
  return <AbsoluteFill style={{ opacity, background: 'white' }}>...</AbsoluteFill>
}
```

Render via `@remotion/lambda` (AWS) ou `@remotion/cloudrun` (GCP) — jamais sur le serveur Next.js.
Docs : https://www.remotion.dev/docs/ai/

---

## Audio — ElevenLabs

```typescript
// app/api/generate-audio/route.ts
const res = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voiceId}`, {
  method: 'POST',
  headers: {
    'xi-api-key': process.env.ELEVENLABS_API_KEY!,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ text, model_id: 'eleven_multilingual_v2' }),
})
const audioBuffer = await res.arrayBuffer()
// Upload vers storage + retourner URL signée
```

---

## Scroll 3D / WebGL

Stack recommandée : `@react-three/fiber` + `@react-three/drei` + `three` + `gsap` (ScrollTrigger) + `lenis`

```bash
pnpm add @react-three/fiber @react-three/drei three gsap lenis
pnpm add -D @types/three
```

```tsx
// Lazy load obligatoire — ne pas bloquer le LCP
const Scene3D = dynamic(() => import('@/components/scene-3d'), {
  ssr: false,
  loading: () => <div className="h-[600px] bg-black animate-pulse" />,
})
```

Règle : canvas 3D en `<Suspense>` + `dynamic` avec `ssr: false`. Jamais de clés API dans le front.

---

## Checklist avant merge

- [ ] Clés API absentes du frontend (Grep `NEXT_PUBLIC_` dans les fichiers API assets)
- [ ] Assets uploadés en storage objet, pas servis depuis `/public`
- [ ] `organizationId` lié en DB si multi-tenant
- [ ] `docs/brand-assets.md` créé ou mis à jour dans le repo application cible
- [ ] Taille des assets vérifiée (images < 200kb WebP, audio < 5MB)

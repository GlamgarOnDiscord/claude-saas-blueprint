# Landing patterns — Code complet

## Hero avec waitlist

```tsx
// app/(marketing)/_components/hero.tsx
'use client'
import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

export function Hero() {
  const [email, setEmail] = useState('')
  const [submitted, setSubmitted] = useState(false)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    await fetch('/api/waitlist', {
      method: 'POST',
      body: JSON.stringify({ email }),
    })
    setSubmitted(true)
    if (typeof window !== 'undefined' && (window as any).posthog) {
      (window as any).posthog.capture('waitlist_signup', { email })
    }
  }

  return (
    <section className="flex flex-col items-start text-left py-24 px-4 gap-6 max-w-4xl">
      <h1 className="text-5xl md:text-7xl font-bold tracking-tight">
        {/* tagline */}
      </h1>
      <p className="text-xl text-muted-foreground max-w-xl">
        {/* sous-titre */}
      </p>
      {!submitted ? (
        <form onSubmit={handleSubmit} className="flex gap-2 w-full max-w-md">
          <Input
            type="email"
            placeholder="ton@email.com"
            value={email}
            onChange={e => setEmail(e.target.value)}
            required
          />
          <Button type="submit">Rejoindre la waitlist</Button>
        </form>
      ) : (
        <p className="text-green-600 font-medium">Tu es sur la liste ✓</p>
      )}
    </section>
  )
}
```

## Route API waitlist

```ts
// app/api/waitlist/route.ts
import { NextResponse } from 'next/server'
import { z } from 'zod'

const Body = z.object({ email: z.string().email() })

export async function POST(req: Request) {
  const parsed = Body.safeParse(await req.json())
  if (!parsed.success) {
    return NextResponse.json(
      { error: { code: 'INVALID_INPUT', message: 'Email invalide' } },
      { status: 400 }
    )
  }

  const { email } = parsed.data
  // Sauver en DB + envoyer confirmation via Resend
  // await db.waitlist.create({ data: { email } })
  return NextResponse.json({ data: { ok: true } })
}
```

## Animations scroll simples

```tsx
// Sans lib externe — fade-in au mount
<div className="opacity-0 translate-y-4 animate-[fadeIn_0.5s_ease_forwards]">
  {/* contenu */}
</div>
```

```css
/* globals.css */
@keyframes fadeIn {
  to { opacity: 1; transform: translateY(0); }
}
```

## Pricing avec plan recommande

```tsx
<div className="grid grid-cols-1 md:grid-cols-3 gap-6">
  {/* Plan basic */}
  <div className="rounded-2xl border border-white/10 bg-zinc-900 p-8">
    <h3 className="text-lg font-semibold">Basic</h3>
    <p className="text-3xl font-bold mt-2">9€<span className="text-sm font-normal">/mo</span></p>
    {/* features list */}
    <Button variant="outline" className="w-full mt-6">Choisir Basic</Button>
  </div>

  {/* Plan recommande */}
  <div className="relative rounded-2xl border-2 border-violet-500 bg-zinc-900 p-8">
    <span className="absolute -top-4 left-1/2 -translate-x-1/2 rounded-full bg-violet-500 px-4 py-1 text-xs font-semibold text-white">
      Le plus populaire
    </span>
    <h3 className="text-lg font-semibold">Pro</h3>
    <p className="text-3xl font-bold mt-2">29€<span className="text-sm font-normal">/mo</span></p>
    <Button className="w-full mt-6">Commencer 14 jours d'essai</Button>
  </div>

  {/* Plan enterprise */}
</div>
```

## SEO meta tags

```tsx
// app/(marketing)/page.tsx
export const metadata = {
  title: 'NomProduit — Tagline en 1 ligne',
  description: 'Description en 155 caracteres max pour Google.',
  openGraph: {
    title: 'NomProduit',
    description: 'Tagline OG',
    images: ['/og-image.png'], // 1200x630
    url: 'https://nomproduit.com',
    siteName: 'NomProduit',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'NomProduit',
    description: 'Tagline twitter',
    images: ['/og-image.png'],
  },
}
```

## Stack 3D / WebGL (si pertinent)

Stack : `@react-three/fiber` + `@react-three/drei` + `three` + `gsap` (ScrollTrigger) + `@studio-freight/lenis`.

Patterns :
- Canvas dans un `<Suspense>` + lazy load
- Cles API generation assets = server-side uniquement (`rules/media-apis.md`)
- Voir `docs/integrations/assets-pipeline.md` section "scroll 3D"

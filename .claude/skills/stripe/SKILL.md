---
name: stripe
description: "Intégration Stripe complète pour SaaS : Checkout, Subscriptions, Webhooks, Customer Portal. Best practices officielles, prêt pour la production."
argument-hint: "- `mode` : checkout | webhooks | subscriptions | portal | setup"
disable-model-invocation: true
---

## Arguments
- `mode` : checkout | webhooks | subscriptions | portal | setup | full

---

## `/stripe setup` — Installation & configuration initiale

```bash
pnpm add stripe @stripe/stripe-js
pnpm add -D @types/stripe
```

**Variables `.env.example` à ajouter :**
```bash
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...   # depuis: stripe listen --forward-to ...
```

**Client Stripe singleton `src/adapters/payments/stripe.ts` :**
```typescript
import Stripe from 'stripe'
export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2026-03-31',   // toujours pin la version API (verifier sur stripe.com)
  typescript: true,
})
```

**CLI local — écouter les webhooks :**
```bash
brew install stripe/stripe-cli/stripe
stripe login
stripe listen --forward-to http://localhost:3000/api/webhooks/stripe
# Copier le whsec_... dans .env.local
```

**Tester des events :**
```bash
stripe trigger invoice.paid
stripe trigger customer.subscription.created
stripe trigger invoice.payment_failed
stripe trigger checkout.session.completed
```

📖 Docs : https://docs.stripe.com/stripe-cli

---

## `/stripe checkout` — Checkout Session (recommandé pour SaaS)

> Utiliser **Checkout Sessions** (pas Payment Intents) sauf besoin de contrôle granulaire.
> Checkout gère automatiquement : taxes, promos, subscriptions, 3D Secure.

**Route API `app/api/checkout/route.ts` :**
```typescript
import { stripe } from '@/adapters/payments/stripe'
import { auth } from '@/adapters/auth'
import { NextResponse } from 'next/server'
import { z } from 'zod'

const Body = z.object({ priceId: z.string() })

export async function POST(req: Request) {
  const session = await auth()
  if (!session) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })

  const { priceId } = Body.parse(await req.json())

  const checkout = await stripe.checkout.sessions.create({
    customer_email: session.user.email,
    client_reference_id: session.user.id,   // lier à votre user
    line_items: [{ price: priceId, quantity: 1 }],
    mode: 'subscription',
    success_url: `${process.env.NEXT_PUBLIC_APP_URL}/billing?success=1`,
    cancel_url:  `${process.env.NEXT_PUBLIC_APP_URL}/billing?canceled=1`,
    automatic_tax: { enabled: true },
    billing_address_collection: 'auto',
    allow_promotion_codes: true,
  })

  return NextResponse.json({ data: { url: checkout.url } })
}
```

**Côté client :**
```typescript
const res = await fetch('/api/checkout', {
  method: 'POST',
  body: JSON.stringify({ priceId: 'price_xxx' }),
})
const { data } = await res.json()
window.location.href = data.url
```

**Cartes de test :**
| Carte | Résultat |
|-------|---------|
| `4242 4242 4242 4242` | Succès |
| `4000 0000 0000 0002` | Refusée |
| `4000 0025 0000 3155` | 3D Secure requis |
| `4000 0000 0000 9995` | Fonds insuffisants |

📖 Docs : https://docs.stripe.com/payments/checkout-sessions-and-payment-intents-comparison

---

## `/stripe webhooks` — Webhooks (critique pour SaaS)

> ⚠️ Utiliser le body **RAW** (pas parsé en JSON) pour la vérification de signature.
> Stocker `event.id` en DB pour l'idempotence (éviter les doubles exécutions).

**Route `app/api/webhooks/stripe/route.ts` :**
```typescript
import { stripe } from '@/adapters/payments/stripe'
import { headers } from 'next/headers'
import { NextResponse } from 'next/server'

// CRITIQUE : désactiver le body parser de Next.js
export const config = { api: { bodyParser: false } }

export async function POST(req: Request) {
  const body      = await req.text()          // RAW — pas req.json()
  const signature = headers().get('stripe-signature')!

  let event: Stripe.Event
  try {
    event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    )
  } catch (err) {
    return NextResponse.json({ error: 'Invalid signature' }, { status: 400 })
  }

  // Idempotence : ignorer si déjà traité
  const alreadyProcessed = await db.stripeEvents.findUnique({ where: { id: event.id } })
  if (alreadyProcessed) return NextResponse.json({ received: true })

  try {
    switch (event.type) {
      case 'checkout.session.completed':
        await handleCheckoutCompleted(event.data.object as Stripe.Checkout.Session)
        break

      case 'invoice.paid':
        // Source de vérité pour les subscriptions actives
        await handleInvoicePaid(event.data.object as Stripe.Invoice)
        break

      case 'invoice.payment_failed':
        await handlePaymentFailed(event.data.object as Stripe.Invoice)
        break

      case 'customer.subscription.updated':
        await handleSubscriptionUpdated(event.data.object as Stripe.Subscription)
        break

      case 'customer.subscription.deleted':
        await handleSubscriptionCanceled(event.data.object as Stripe.Subscription)
        break
    }

    // Marquer comme traité
    await db.stripeEvents.create({ data: { id: event.id, type: event.type } })
  } catch (err) {
    // Retourner 500 → Stripe retentera automatiquement
    return NextResponse.json({ error: 'Handler failed' }, { status: 500 })
  }

  return NextResponse.json({ received: true })
}
```

**Events critiques à écouter (SaaS) :**
| Event | Action |
|-------|--------|
| `checkout.session.completed` | Créer/lier customer + subscription en DB |
| `invoice.paid` | ✅ Activer l'accès / renouveler |
| `invoice.payment_failed` | ⚠️ Restreindre l'accès, notifier |
| `customer.subscription.updated` | Sync plan en DB |
| `customer.subscription.deleted` | Désactiver l'accès |

📖 Docs : https://docs.stripe.com/webhooks/handling-payment-events | https://docs.stripe.com/webhooks/signature

---

## `/stripe subscriptions` — Gestion des abonnements

**États possibles :**
```
trialing   → Essai gratuit en cours
active     → Abonnement actif et à jour
past_due   → Paiement échoué, retry en cours
paused     → Suspendu
canceled   → Annulé
```

**Upgrade / Downgrade avec proration :**
```typescript
// Changer de plan immédiatement avec facture de proration
await stripe.subscriptions.update(subscriptionId, {
  items: [{ id: subscriptionItemId, price: 'price_premium' }],
  proration_behavior: 'always_invoice',  // génère facture immédiate
})
```

**Créer avec période d'essai :**
```typescript
await stripe.subscriptions.create({
  customer: customerId,
  items: [{ price: 'price_xxx' }],
  trial_period_days: 14,
})
```

**Annuler (fin de période vs immédiat) :**
```typescript
// Fin de la période actuelle (recommandé UX)
await stripe.subscriptions.update(subscriptionId, {
  cancel_at_period_end: true,
})

// Immédiat
await stripe.subscriptions.cancel(subscriptionId)
```

📖 Docs : https://docs.stripe.com/billing/subscriptions/overview | https://docs.stripe.com/billing/subscriptions/upgrade-downgrade

---

## `/stripe portal` — Customer Portal

**Route `app/api/billing/portal/route.ts` :**
```typescript
import { stripe } from '@/adapters/payments/stripe'
import { auth } from '@/adapters/auth'
import { NextResponse } from 'next/server'

export async function POST() {
  const session = await auth()
  if (!session) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })

  // Récupérer le stripeCustomerId depuis votre DB
  const user = await db.users.findUnique({ where: { id: session.user.id } })
  if (!user?.stripeCustomerId) {
    return NextResponse.json({ error: 'No billing account' }, { status: 404 })
  }

  const portal = await stripe.billingPortal.sessions.create({
    customer: user.stripeCustomerId,
    return_url: `${process.env.NEXT_PUBLIC_APP_URL}/billing`,
  })

  return NextResponse.json({ data: { url: portal.url } })
}
```

Le Customer Portal gère automatiquement : changement de plan, annulation, mise à jour CB, historique des factures.

📖 Docs : https://docs.stripe.com/customer-management/integrate-customer-portal

---

## Schema DB recommandé (Drizzle)

```typescript
// Table subscriptions liée à organizations
export const subscriptions = pgTable('subscriptions', {
  id:                   uuid('id').defaultRandom().primaryKey(),
  organizationId:       uuid('organization_id').references(() => organizations.id),
  stripeCustomerId:     text('stripe_customer_id').unique(),
  stripeSubscriptionId: text('stripe_subscription_id').unique(),
  stripePriceId:        text('stripe_price_id'),
  stripeCurrentPeriodEnd: timestamp('stripe_current_period_end'),
  status:               text('status'),  // active | trialing | past_due | canceled
  plan:                 text('plan'),    // free | pro | enterprise
  createdAt:            timestamp('created_at').defaultNow(),
  updatedAt:            timestamp('updated_at').defaultNow(),
})

// Table pour l'idempotence des webhooks
export const stripeEvents = pgTable('stripe_events', {
  id:          text('id').primaryKey(),   // event.id de Stripe
  type:        text('type'),
  processedAt: timestamp('processed_at').defaultNow(),
})
```

---

## Checklist pré-production

- [ ] Clés `sk_live_` + `pk_live_` configurées dans Vercel (pas les sk_test_)
- [ ] Webhook endpoint enregistré dans Stripe Dashboard → Developers → Webhooks
- [ ] `STRIPE_WEBHOOK_SECRET` en prod différent du local (`whsec_...`)
- [ ] RLS sur `subscriptions` table (par `organization_id`)
- [ ] Test avec `stripe trigger` sur l'env staging avant prod
- [ ] Customer Portal activé dans Stripe Dashboard → Billing → Customer Portal

📖 Docs officielles complètes : https://docs.stripe.com/billing/subscriptions/build-subscriptions

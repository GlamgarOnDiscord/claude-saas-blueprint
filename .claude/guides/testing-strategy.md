# Stratégie de Testing

## Pyramide de Tests SaaS

```
         /  E2E  \        ← 5-10 tests : parcours critiques (signup, paiement)
        / Intégration \    ← 20-30 tests : API endpoints, DB queries
       /    Unitaire    \  ← 50+ tests : usecases, validation, utils
```

## Que Tester en Priorité

### Toujours tester (non négociable)
1. **Use Cases** (core/usecases/) — C'est la logique métier, c'est le coeur
2. **Validation schemas** (Zod) — Vérifier les cas limites
3. **Auth middleware** — Vérifier que les routes sont protégées
4. **Paiements** — Vérifier les webhooks Stripe, les changements de plan

### Tester si le temps le permet
5. **Repositories** (tests d'intégration avec DB test)
6. **API endpoints** (tests d'intégration HTTP)
7. **Composants UI critiques** (formulaires, modals de confirmation)

### Ne PAS tester (perte de temps)
- Composants UI purement visuels (utiliser un screenshot test si besoin)
- Getters/setters triviaux
- Code de configuration
- Ce que le framework teste déjà (routing, rendering)

## Convention de Nommage
```
src/core/usecases/create-invoice.ts
src/core/usecases/__tests__/create-invoice.test.ts

src/adapters/api/invoices/route.ts
src/adapters/api/invoices/__tests__/route.test.ts
```

## Structure d'un Test
```typescript
describe('[Use Case] create-invoice', () => {
  // Arrange — Setup commun
  const mockRepo = { create: vi.fn(), findById: vi.fn() };

  it('should create an invoice with valid data', async () => {
    // Arrange — Setup spécifique
    // Act — Exécuter
    // Assert — Vérifier
  });

  it('should reject if amount is negative', async () => {
    // Test du cas d'erreur
  });

  it('should enforce organization isolation', async () => {
    // Test multi-tenancy
  });
});
```

## Outils par Stack
| Stack | Unit | Integration | E2E |
|-------|------|-------------|-----|
| Next.js | Vitest | Vitest + supertest | Playwright |
| Remix | Vitest | Vitest | Playwright |
| FastAPI | pytest | pytest + httpx | pytest + Playwright |
| Go | testing | testing + testcontainers | Playwright |

## Coverage Targets
- **Core** (usecases, entities) : > 80%
- **Adapters** (API, DB) : > 60%
- **Global** : > 60%
- Ne JAMAIS sacrifier la qualité des tests pour le coverage

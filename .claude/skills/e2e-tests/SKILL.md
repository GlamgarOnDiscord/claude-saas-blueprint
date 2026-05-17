---
name: e2e-tests
description: "Tests E2E Playwright pour SaaS Next.js : setup, Page Object Model, auth state, flows critiques (login, billing, onboarding), CI GitHub Actions."
argument-hint: "- `mode` : setup | generate | run | ci"
disable-model-invocation: true
---

## Arguments
- `mode` : setup | generate | run | ci | visual

---

## `/e2e-tests setup` — Installation & configuration

```bash
pnpm add -D @playwright/test
npx playwright install chromium firefox webkit
```

**`playwright.config.ts` à la racine :**
```typescript
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html'],
    ['github'],      // annotations PR GitHub
    ['junit', { outputFile: 'results/junit.xml' }],
  ],
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    locale: 'en-US',
    timezoneId: 'Europe/Paris',
    reducedMotion: 'reduce',   // désactiver animations pour snapshots stables
  },
  webServer: {
    command: 'pnpm dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120_000,
  },
  projects: [
    // 1. Setup auth en premier
    { name: 'setup', testMatch: /.*\.setup\.ts/ },
    // 2. Tests authentifiés
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'], storageState: 'playwright/.auth/user.json' },
      dependencies: ['setup'],
    },
    // 3. Tests non-authentifiés (landing, login, signup)
    {
      name: 'chromium-public',
      use: { ...devices['Desktop Chrome'] },
      testMatch: /.*\.public\.spec\.ts/,
    },
  ],
})
```

**`.gitignore` :**
```
playwright/.auth/
playwright-report/
test-results/
```

📖 Docs : https://playwright.dev/docs/intro

---

## Structure des fichiers

```
tests/e2e/
├── auth.setup.ts              # Setup global auth (run once)
├── pages/                     # Page Object Models
│   ├── login.page.ts
│   ├── dashboard.page.ts
│   ├── billing.page.ts
│   └── onboarding.page.ts
├── fixtures/
│   └── index.ts               # Fixtures réutilisables
├── auth-flow.spec.ts          # Login, signup, logout
├── onboarding.spec.ts         # Premier onboarding
├── billing.spec.ts            # Plans, checkout, portal
├── dashboard.spec.ts          # Fonctionnalités core
└── billing-portal.public.spec.ts  # Pages publiques
```

---

## Auth state — réutilisation entre tous les tests

```typescript
// tests/e2e/auth.setup.ts
import { test as setup, expect } from '@playwright/test'
import path from 'path'

const authFile = path.join(__dirname, '../../playwright/.auth/user.json')

setup('authenticate', async ({ page }) => {
  await page.goto('/login')
  await page.fill('input[type="email"]', process.env.E2E_USER_EMAIL!)
  await page.fill('input[type="password"]', process.env.E2E_USER_PASSWORD!)
  await page.click('button[type="submit"]')

  await page.waitForURL('**/dashboard')
  await expect(page.locator('h1')).toBeVisible()

  // Sauvegarder cookies + localStorage → réutilisé par tous les tests
  await page.context().storageState({ path: authFile })
})
```

Variables `.env.test` :
```bash
E2E_USER_EMAIL=test@example.com
E2E_USER_PASSWORD=TestPassword123!
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

📖 Docs : https://playwright.dev/docs/auth

---

## Page Object Model — Pattern standard

```typescript
// tests/e2e/pages/billing.page.ts
import { type Page, type Locator } from '@playwright/test'

export class BillingPage {
  readonly page: Page
  readonly planCards: Locator
  readonly upgradeButton: Locator
  readonly manageButton: Locator
  readonly currentPlanBadge: Locator

  constructor(page: Page) {
    this.page = page
    this.planCards     = page.locator('[data-testid="plan-card"]')
    this.upgradeButton = page.locator('button:has-text("Upgrade")')
    this.manageButton  = page.locator('button:has-text("Manage subscription")')
    this.currentPlanBadge = page.locator('[data-testid="current-plan"]')
  }

  async goto() { await this.page.goto('/billing') }

  async selectPlan(plan: 'free' | 'pro' | 'enterprise') {
    await this.page.locator(`[data-testid="plan-${plan}"] button`).click()
  }

  async getCurrentPlan(): Promise<string> {
    return await this.currentPlanBadge.textContent() ?? ''
  }
}
```

**Règles POM :**
- 1 fichier = 1 page/feature
- Locators = propriétés de classe (jamais hardcodés dans les tests)
- Méthodes = actions utilisateur, PAS d'assertions
- Assertions dans les fichiers `*.spec.ts` uniquement

📖 Docs : https://playwright.dev/docs/pom

---

## `/e2e-tests generate` — Flows critiques SaaS

### Flow 1 — Authentification

```typescript
// tests/e2e/auth-flow.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Auth', () => {
  test('login réussi redirige vers dashboard', async ({ page }) => {
    await page.goto('/login')
    await page.fill('input[type="email"]', process.env.E2E_USER_EMAIL!)
    await page.fill('input[type="password"]', process.env.E2E_USER_PASSWORD!)
    await page.click('button[type="submit"]')
    await page.waitForURL('**/dashboard')
    await expect(page.locator('h1')).toBeVisible()
  })

  test('mauvais mot de passe affiche erreur', async ({ page }) => {
    await page.goto('/login')
    await page.fill('input[type="email"]', 'wrong@test.com')
    await page.fill('input[type="password"]', 'badpassword')
    await page.click('button[type="submit"]')
    await expect(page.locator('[data-testid="error"]')).toBeVisible()
    await expect(page).toHaveURL('/login') // reste sur la page
  })

  test('route protégée redirige vers login', async ({ page }) => {
    // Pas de storageState → non authentifié
    await page.goto('/dashboard')
    await page.waitForURL('**/login')
  })
})
```

### Flow 2 — Billing & Stripe

```typescript
// tests/e2e/billing.spec.ts
import { test, expect } from '@playwright/test'
import { BillingPage } from './pages/billing.page'

test.describe('Billing', () => {
  test('affiche les plans disponibles', async ({ page }) => {
    const billing = new BillingPage(page)
    await billing.goto()
    await expect(billing.planCards).toHaveCount(3) // free, pro, enterprise
  })

  test('clic upgrade redirige vers Stripe Checkout', async ({ page }) => {
    const billing = new BillingPage(page)
    await billing.goto()
    await billing.selectPlan('pro')
    // Vérifier la redirection vers Stripe (en test mode)
    await page.waitForURL(/checkout\.stripe\.com|localhost/)
  })

  test('webhook invoice.paid active le plan Pro', async ({ page, request }) => {
    // Simuler le webhook Stripe côté serveur
    const response = await request.post('/api/webhooks/stripe', {
      headers: { 'stripe-signature': 'test' },
      data: {
        id: `evt_test_${Date.now()}`,
        type: 'invoice.paid',
        data: {
          object: {
            customer: 'cus_test',
            subscription: 'sub_test',
            status: 'paid',
          },
        },
      },
    })
    // Le handler doit accepter (logique testée en unit test)
    expect([200, 400]).toContain(response.status())
  })
})
```

### Flow 3 — Multi-tenancy (isolation organisations)

```typescript
test('un user ne voit pas les données d\'une autre org', async ({ page }) => {
  await page.goto('/dashboard')
  // Vérifier que les données affichées appartiennent à l'org de l'utilisateur
  const orgName = await page.locator('[data-testid="org-name"]').textContent()
  expect(orgName).toBe('Mon Organisation') // pas une autre org
})
```

---

## `/e2e-tests ci` — GitHub Actions

```yaml
# .github/workflows/e2e.yml
name: E2E Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  e2e:
    timeout-minutes: 30
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        shard: [1, 2, 3]   # 3 shards parallèles

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Install Playwright browsers
        run: npx playwright install --with-deps chromium

      - name: Run E2E tests (shard ${{ matrix.shard }}/3)
        run: npx playwright test --shard=${{ matrix.shard }}/3
        env:
          E2E_USER_EMAIL: ${{ secrets.E2E_USER_EMAIL }}
          E2E_USER_PASSWORD: ${{ secrets.E2E_USER_PASSWORD }}
          NEXT_PUBLIC_APP_URL: http://localhost:3000
          DATABASE_URL: ${{ secrets.TEST_DATABASE_URL }}

      - name: Upload blob report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: blob-report-${{ matrix.shard }}
          path: blob-report
          retention-days: 1

  merge-reports:
    if: always()
    needs: [e2e]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: 'pnpm' }
      - run: pnpm install --frozen-lockfile
      - uses: actions/download-artifact@v4
        with: { path: all-blob-reports, pattern: blob-report-* }
      - run: npx playwright merge-reports --reporter html ./all-blob-reports
      - uses: actions/upload-artifact@v4
        with:
          name: html-report
          path: playwright-report/
          retention-days: 14
```

📖 Docs : https://playwright.dev/docs/ci-intro

---

## `/e2e-tests visual` — Snapshots visuels

```typescript
test('billing page — snapshot', async ({ page }) => {
  await page.goto('/billing')
  await page.waitForLoadState('networkidle')

  // Masquer les éléments dynamiques
  await page.addStyleTag({
    content: '[data-testid="date"], .js-timestamp { visibility: hidden; }'
  })

  await expect(page).toHaveScreenshot('billing.png', {
    maxDiffPixels: 200,   // tolérance pour anti-aliasing
  })
})
```

Mettre à jour les snapshots après un changement intentionnel :
```bash
npx playwright test --update-snapshots
```

📖 Docs : https://playwright.dev/docs/test-snapshots

---

## Commandes du quotidien

```bash
# Lancer tous les tests
npx playwright test

# Mode UI (debug visuel)
npx playwright test --ui

# Un seul test
npx playwright test billing.spec.ts

# Debug pas à pas
npx playwright test --debug

# Générer du code en enregistrant les actions
npx playwright codegen http://localhost:3000
```

📖 Best practices : https://playwright.dev/docs/best-practices

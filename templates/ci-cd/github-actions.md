# Template: GitHub Actions CI/CD

## CI — Pull Request
```yaml
# .github/workflows/ci.yml
name: CI
on:
  pull_request:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v2  # ou setup-node
      - run: bun install --frozen-lockfile
      - run: bun run lint
      - run: bun run typecheck
      - run: bun test --coverage
      - run: bun run build
```

## CD — Deploy on Merge
```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v2
      - run: bun install --frozen-lockfile
      - run: bun run build
      # Deploy step selon le provider (Vercel, Railway, etc.)
```

## DB Migrations
```yaml
# .github/workflows/migrate.yml
name: DB Migration
on:
  push:
    branches: [main]
    paths: ['src/adapters/db/migrations/**']

jobs:
  migrate:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v2
      - run: bun install --frozen-lockfile
      - run: bun run db:migrate
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

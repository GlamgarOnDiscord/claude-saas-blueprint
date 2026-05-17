# Rules: Tests

## Obligatoire
- Suivre le pattern AAA : Arrange, Act, Assert
- Tester le happy path ET les cas d'erreur
- Toujours tester l'isolation multi-tenant (organizationId)
- Mocker les dépendances externes (DB, API, email), jamais le code interne
- Nommer les tests avec "should [verbe] when [condition]"

## Interdit
- Ne PAS tester l'implémentation interne — tester le comportement
- Ne PAS créer de tests qui dépendent de l'ordre d'exécution
- Ne PAS utiliser `any` dans les types de test — typer les mocks
- Ne PAS oublier le cleanup (afterEach, afterAll)

## Learned
<!-- Règles ajoutées automatiquement par l'agent -->

# Hook: SessionStart (matcher: compact) — recharge le contexte projet apres /compact.
# Sortie stdout ajoutee au contexte de la session.

@'
[CONTEXTE RECHARGE APRES COMPACTION]
- Stack: Next.js 15 + Supabase + Vercel (par defaut, peut varier selon projet)
- Architecture: hexagonale (core / adapters / shared)
- Conventions: kebab-case fichiers, PascalCase types, max 200 lignes/fichier
- Securite: RLS sur toutes les tables, Zod au boundary, secrets jamais commits
- Workflow: APEX (Analyze / Plan / Execute / eXamine)
- Reponses en francais.
'@ | Write-Output

exit 0

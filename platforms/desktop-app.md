# Platform: Desktop Application

## Stacks Recommandées (2026)

### Option A — Tauri 2 (Recommandé)
- **Framework**: Tauri 2 + React/Svelte frontend
- **Backend**: Rust (natif, performant, sécurisé)
- **UI**: Web stack (Tailwind + shadcn ou similaire)
- **Storage**: SQLite via rusqlite ou Tauri SQL plugin
- **Auto-update**: Tauri Updater
- **Build**: Cross-platform (Windows, macOS, Linux)
- **Taille**: ~5-10MB (vs 100MB+ Electron)

### Option B — Electron
- Si l'écosystème npm est critique ou équipe web-only
- Attention : bundle lourd, RAM intensive

### Option C — Flutter Desktop
- Si le projet est déjà Flutter mobile

## Conventions Desktop
- Raccourcis clavier natifs (Cmd/Ctrl+S, etc.)
- Menu système natif
- Tray icon si app background
- Auto-update silencieux
- Multi-window si pertinent
- File system access natif
- Respecter les conventions OS (titlebars, dialogs)

## Structure Tauri Recommandée
```
src-tauri/
├── src/
│   ├── main.rs           # Entry point Rust
│   ├── commands/         # IPC commands
│   └── lib.rs
├── Cargo.toml
└── tauri.conf.json
src/                      # Frontend (même structure web)
├── core/
├── adapters/
├── components/
└── lib/
```

## Checklist Desktop
- [ ] Installer / Uninstaller
- [ ] Auto-update
- [ ] Code signing (Windows + macOS)
- [ ] Notarization macOS
- [ ] Raccourcis clavier
- [ ] Menu système
- [ ] Deep linking / URL scheme
- [ ] Crash reporting
- [ ] Taille du bundle optimisée

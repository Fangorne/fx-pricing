# Plan — run-fx-pricing-010

## Work Item: frontend-scaffold
**Mode**: autopilot | **Complexity**: low

---

## Approach

Scaffolding manuel du projet frontend avec Vite 5 + React 18 + TypeScript strict + Tailwind CSS 3.
On n'utilise pas `create-vite` (non interactif en CI) — on génère tous les fichiers directement.

Structure cible :
```
frontend/
├── index.html
├── vite.config.ts
├── tsconfig.json
├── tsconfig.node.json
├── tailwind.config.js
├── postcss.config.js
├── eslint.config.js
├── .prettierrc
├── .env.local
├── package.json
└── src/
    ├── main.tsx
    ├── App.tsx
    ├── index.css
    ├── types/
    │   └── fx.ts
    ├── services/
    │   └── api.ts
    ├── components/
    ├── features/
    ├── hooks/
    └── store/
```

## Files to Create

- `frontend/package.json` — deps pnpm (react, vite, tailwind, vitest, eslint, prettier)
- `frontend/index.html` — entry point HTML
- `frontend/vite.config.ts` — Vite config avec path alias `@/`
- `frontend/tsconfig.json` — TypeScript strict
- `frontend/tsconfig.node.json` — TS config pour vite.config.ts
- `frontend/tailwind.config.js` — Tailwind config
- `frontend/postcss.config.js` — PostCSS avec tailwind + autoprefixer
- `frontend/eslint.config.js` — ESLint 9 flat config TypeScript
- `frontend/.prettierrc` — Prettier config
- `frontend/.env.local` — VITE_API_BASE_URL
- `frontend/src/main.tsx` — entry point React
- `frontend/src/App.tsx` — App root avec Tailwind
- `frontend/src/index.css` — directives Tailwind
- `frontend/src/types/fx.ts` — types domaine FX
- `frontend/src/services/api.ts` — client API fetch

## Files to Modify

- `docker-compose.yml` — ajout service `frontend`

## Tests

- `pnpm install && pnpm build` — validation TypeScript
- `pnpm lint` — ESLint + Prettier
- `pnpm test` — Vitest (0 tests collectés = OK)

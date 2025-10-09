This repository is a small React TypeScript front-end (UI components under `src/componets`) for the GrimoireGame project. Additions and fixes should follow the concrete patterns below so automated agents remain productive.

Quick context
- UI is component-driven under `src/componets/*`. Note the folder name is `componets` (misspelling) — follow it when referencing or creating files.
- Styling uses Tailwind-style utility classes directly in `className` (see `src/componets/views/HomeView.tsx`).
- Icons are provided by `lucide-react` (see imports in `HomeView.tsx`).
- There is no `package.json` or build config in the repository root visible in the workspace; assume this is a partial snapshot. Before generating buildable code, confirm package and tooling choices with the maintainer.

How to modify UI components
- Keep files under `src/componets/*` to match current project layout. Don't create `src/components` (the more common spelling) unless asked — doing so will break imports.
- Use Tailwind utility classes inline. Example: grid and color usage in `HomeView.tsx` — preserve the same naming (`font-serif`, `from-amber-700`, etc.).
- Follow the data surface shown in `HomeView.tsx`: components expect typed props like `setCurrentView: (view: Screen) => void` and `userGames: Game[]` imported from `../../types`. If `types` are missing, add minimal compatible types in `src/types.ts` rather than changing callers.

Patterns & examples
- Game card pattern (from `HomeView.tsx`): clickable container that sets `setSelectedGame(game)` and `setCurrentView('quest')`. Keep that behavior when extracting or refactoring.
- Difficulty styling is a colors map object in `HomeView.tsx` — prefer centralizing similar maps into `src/constants/*` only after confirming with author.
- Decorative/visual elements (blurred circles, gradients) are implemented directly with Tailwind and inline style objects; preserve inline styles for small effects.

Behavioral expectations
- Navigation is handled by view-state callbacks rather than a router (see `setCurrentView` usage). When adding navigation, keep the existing view enum (`Screen`) and update callers.
- Components should be small and focused; when creating new shared components, place them under `src/componets/common/` and export with clear prop-types (TS interfaces).

Missing or uncertain items (ask before changing)
- Build/test scripts and package manifest: there is no `package.json` or `tsconfig.json` in the workspace snapshot. Ask the maintainer for preferred package manager (npm/pnpm/yarn), Node version, and any monorepo constraints before adding tooling.
- `src/types` referred in `HomeView.tsx` exists in imports but wasn't found in this snapshot — confirm its location/shape before changing type names.

Quick rules for automated edits
1. Never rename `componets` to `components`. Follow the repo's existing import paths.
2. Preserve Tailwind class patterns and color names used in `HomeView.tsx` and other files to keep a consistent theme.
3. If adding new shared code, keep it under `src/componets/common/` and export with TypeScript interfaces.
4. If you must add tooling files (`package.json`, `tsconfig.json`), first leave a draft PR and request confirmation — do not assume package choices.

Where to look first
- `src/componets/views/HomeView.tsx` — primary example of component, styling, icon usage, prop shapes.
- `src/componets/common/*` — shared component folder (some files may be placeholders).
- `README.md` — small project summary: "Scans games and helps give strategies to stat trees, boss fights, etc."

If anything is ambiguous, ask the maintainer these quick questions:
- Where is the project root package.json / preferred package manager?
- Confirm whether renaming `componets` to `components` is acceptable.
- Provide `src/types.ts` or the expected shapes for `Screen` and `Game`.

Feedback request
If you'd like, I can expand this file with examples (type stubs for `Screen`/`Game`, a suggested minimal `package.json`, or a migration plan to rename `componets`). Tell me which you'd prefer.

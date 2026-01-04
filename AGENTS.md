# Repository Guidelines

## Project Structure & Module Organization
- `auth-layer/`: TypeScript authentication layer (source in `auth-layer/src/`, build output in `auth-layer/dist/`).
- `plugins/notebooklm/`: Claude Code plugin assets, skills, and commands.
- `mcp-config/`: MCP server config templates and install scripts.
- `docs/`: Setup guides and troubleshooting references.
- `tests/`: Simulation tooling (`run_simulation.py`) used to validate user flows.

## Build, Test, and Development Commands
Run commands from the relevant subdirectory.
- `cd auth-layer && npm install`: install dependencies.
- `cd auth-layer && npm run build`: compile TypeScript to `dist/`.
- `cd auth-layer && npm run dev`: watch mode for local development.
- `cd auth-layer && npm run lint`: run ESLint on `src/`.
- `cd auth-layer && npm test`: run Node’s built-in test runner.
- `python3 tests/run_simulation.py`: run the end-to-end NotebookLM CLI simulation.

## Coding Style & Naming Conventions
- TypeScript in `auth-layer/` uses ESM (`"type": "module"`) and 2-space indentation (match existing files).
- Prefer explicit, descriptive names for backends and auth helpers (e.g., `CDPAuthBackend`).
- Keep CLI commands in `auth-layer/src/cli.ts` and shared types in `auth-layer/src/types.ts`.
- Use `npm run lint` before committing changes in `auth-layer/`.

## Testing Guidelines
- Unit tests (if added) should live near the `auth-layer/src/` code or in a dedicated `auth-layer/test/` folder and be runnable via `npm test`.
- Simulation tests are in `tests/` and should be kept scriptable (no manual prompts).
- Name tests to reflect the behavior under test (e.g., `auth-manager.test.ts`).

## Commit & Pull Request Guidelines
- Commit messages follow imperative, sentence-case style (e.g., "Add NotebookLM plugin for Claude Code").
- PRs should include a short description, test command(s) run, and any setup notes.
- Link related issues when applicable and include screenshots or logs for UX or CLI output changes.

## Security & Configuration Tips
- Do not commit secrets. Use `mcp-config/env.example` as the template for environment values.
- Auth data may rely on local keychain or browser profiles; document any new storage locations.

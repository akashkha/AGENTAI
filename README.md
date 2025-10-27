# Playwright project for AgentAI

This folder contains a minimal Playwright Test setup.

Quick start (PowerShell on Windows):

```powershell
cd E:\AgentAI
npm install --save-dev @playwright/test
npx playwright install --with-deps
npx playwright test
```

Useful npm scripts (defined in package.json):
- `npm run test` — run tests (headless)
- `npm run test:headed` — run tests with a visible browser
- `npm run install-browsers` — install Playwright browsers and dependencies

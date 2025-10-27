const { test, expect } = require('@playwright/test');

test('example.com has expected title', async ({ page }) => {
  await page.goto('https://example.com');
  await expect(page).toHaveTitle(/Example Domain/);
});

import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('https://rabata.io/');
  await page.getByRole('banner').getByRole('link', { name: 'Calculator' }).click();
  await page.locator('#dataApiStoredInput').fill('501');
  await page.locator('#dataApiStoredInput').click();
});
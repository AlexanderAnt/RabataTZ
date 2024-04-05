import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('https://rabata.io/');
  await page.getByRole('banner').getByRole('link', { name: 'Calculator' }).click();
  await page.getByText('$59 S3 compatible hot-backup for $59 per 10 TB of storage. Backup').click();
  await page.locator('#dataStoredInput').fill('501');
  await page.locator('#dataStoredInput').click();
});
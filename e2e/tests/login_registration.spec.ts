import { test, expect } from '@playwright/test';

const BASE_URL = process.env.BASE_URL || 'https://xbpneus-frontend.onrender.com';

test.describe('Authentication', () => {
  test('login page loads and has sign up link', async ({ page }) => {
    await page.goto(BASE_URL + '/');
    // Check for email and password inputs
    await expect(page.locator('input[type="email"]')).toBeVisible();
    await expect(page.locator('input[type="password"]')).toBeVisible();
    // Check that the sign-up link is visible
    await expect(page.locator('text=Quero me cadastrar')).toBeVisible();
  });

  test('registration page shows all user types', async ({ page }) => {
    await page.goto(BASE_URL + '/');
    await page.click('text=Quero me cadastrar');
    await expect(page).toHaveURL(/cadastro/);
    const dropdown = page.locator('select');
    // Open dropdown to ensure options are loaded
    await dropdown.click();
    const options = dropdown.locator('option');
    const values = await options.allTextContents();
    expect(values).toEqual(expect.arrayContaining([
      'Transportador',
      'Motorista',
      'Revenda',
      'Borracharia',
      'Recapagem',
    ]));
  });
});

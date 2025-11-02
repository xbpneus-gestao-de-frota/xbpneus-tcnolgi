import { test, expect } from '@playwright/test';

// Ajuste esta lista conforme os itens reais do menu lateral do seu front
const menuItems = [
  'Dashboard',
  'Compras',
  'Fornecedores',
  'Financeiro',
  'Pagar',
  'Receber',
  'Fluxo',
  'Estoque',
  'Vendas',
  'Borracharia'
];

test('navegação pelos itens do menu lateral', async ({ page }) => {
  await page.goto('/');
  for (const item of menuItems) {
    const link = page.getByRole('link', { name: item }).first();
    if (await link.count()) {
      await link.click();
      await expect(page).toHaveURL(/.+/);
      const anyHeading = page.getByRole('heading', { name: new RegExp(item, 'i') });
      if (await anyHeading.count()) {
        await expect(anyHeading.first()).toBeVisible();
      }
      await page.waitForTimeout(200);
    }
  }
});
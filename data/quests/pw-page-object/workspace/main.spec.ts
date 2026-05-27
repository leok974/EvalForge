import { test, expect, Page } from '@playwright/test';

// TODO: Create a LoginPage class with:
//   - constructor(page: Page)
//   - async login(username: string, password: string): Promise<void>
//     which fills the form and clicks submit

// Placeholder class (incomplete):
class LoginPage {
  constructor(private page: Page) {}

  async navigate() {
    await this.page.goto('/login');
  }

  // TODO: add async login(username, password) method
}

test('login using page object', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.navigate();
  // TODO: call loginPage.login('admin', 'secret123')
  // then assert URL contains /dashboard
  await expect(page).toHaveURL('/login'); // wrong - should redirect
});

import { Page, Locator } from '@playwright/test';

export class RabataSignup {
  page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  async inputFullName(fullName: string) {
    const fullNameInput = await this.page.locator('#registration_form_fullName');
    await fullNameInput.type(fullName);
  }

  async inputEmail(email: string) {
    const emailInput = await this.page.locator('#registration_form_email');
    await emailInput.type(email);
  }

  async inputPassword(password: string) {
    const passwordInput = await this.page.locator('#registration_form_plainPassword_first');
    await passwordInput.type(password);
  }

  async inputConfirmPassword(confirmPassword: string) {
    const confirmPasswordInput = await this.page.locator('#registration_form_plainPassword_second');
    await confirmPasswordInput.type(confirmPassword);
  }

async checkAgreeTerms() {
        const agreeTermsLabel = await this.page.locator('label[for="registration_form_agreeTerms"]');
        await agreeTermsLabel.click();  
}
  
  async clickSignUpButton() {
    const signUpButton = await this.page.locator('.btn-login');
    await signUpButton.click();
  }

  async clickLoginLink() {
    const loginLink = await this.page.waitForSelector('//a[contains(text(),"Log in")]');
    await loginLink.click();
}

}

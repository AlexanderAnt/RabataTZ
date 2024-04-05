import { Page } from '@playwright/test';

export class RabataMain {
  page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  async open() {
    await this.page.goto('https://rabata.io/');
  }

  async getTitle() {
    return await this.page.title();
  }

  async getUrl() {
    return await this.page.url();
  }

  async clickSignUpLink() {
    const signUpLink = await this.page.locator("//a[@class='header-signup' and text()='Sign Up']");
    await signUpLink.click();
  }

  async clickTryItForFreeButton() {
    const tryItForFreeButton = await this.page.waitForSelector('//a[contains(text(),"Try it for free")]');
    await tryItForFreeButton.click();
}

async clickPrivacyPolicy() {
  const privacyPolicyLink = await this.page.waitForSelector("//a[contains(text(),'Privacy policy')]");
  await privacyPolicyLink.click();
}
  

}

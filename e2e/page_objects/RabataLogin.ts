import { Page } from 'playwright';

export class RabataLogin {
    private page: Page;

    constructor(page: Page) {
        this.page = page;
    }

    async inputUsername(username: string) {
        const usernameField = await this.page.waitForSelector('//input[@id="username"]');
        await usernameField.fill(username);
    }

    async inputPassword(password: string) {
        const passwordField = await this.page.waitForSelector('//input[@id="password"]');
        await passwordField.fill(password);
    }

    async clickLoginButton() {
        const loginButton = await this.page.waitForSelector('//button[contains(text(),"Log in")]');
        await loginButton.click();
    }
}

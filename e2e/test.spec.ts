import { test, expect } from '@playwright/test';
import { RabataMain } from './page_objects/RabataMain';
import { RabataSignup } from './page_objects/RabataSignup';
import { RabataLogin } from './page_objects/RabataLogin';
import Chance from 'chance';
import { PrivacyPolicy } from './page_objects/PrivacyPolicy';

test.describe('Rabata Website', () => {
  test('Sign up on Rabata website', async ({ page }) => {
    const rabataMain = new RabataMain(page);
    const signupPage = new RabataSignup(page);
    await rabataMain.open();
    await rabataMain.clickSignUpLink();
    await page.waitForLoadState('domcontentloaded');
    await page.waitForLoadState('networkidle');
    const chance = new Chance();
    const randomEmail = chance.email();
    await signupPage.inputFullName('Jon Snow');
    await signupPage.inputEmail(randomEmail);
    await signupPage.inputPassword('Password123!');
    await signupPage.inputConfirmPassword('Password123!');
    await signupPage.checkAgreeTerms();
    await signupPage.clickSignUpButton();
    await page.waitForSelector(`//a[contains(text(),'${randomEmail}')]`);
    const emailLink = await page.$(`//a[contains(text(),'${randomEmail}')]`);
    expect(emailLink).not.toBeNull();
    const verifyEmailHeader = await page.$(`//h1[contains(text(),'Verify your email')]`);
    expect(verifyEmailHeader!).toBeTruthy();
    const currentUrl = page.url();
    expect(currentUrl).toContain('https://rabata.io/verify/info/');
  });

  test('Try it free for registred user', async ({ page }) => {
    const rabataMain = new RabataMain(page);
    const signupPage = new RabataSignup(page);
    const loginPage = new RabataLogin(page);
    await rabataMain.open();
    await rabataMain.clickTryItForFreeButton(); 
    await signupPage.clickLoginLink();
    await loginPage.inputUsername('antonovalexandr88@gmail.com');
    await loginPage.inputPassword('Qwerty!23');
    await loginPage.clickLoginButton();
    const currentUrl = page.url();
    expect(currentUrl).toContain('https://rabata.io/dashboard');
  });

  test('Try it free for non-registred user', async ({ page }) => {
    const rabataMain = new RabataMain(page);
    const signupPage = new RabataSignup(page);
    await rabataMain.open();
    await rabataMain.clickTryItForFreeButton(); 
    const chance = new Chance();
    const randomEmail = chance.email();
    await signupPage.inputFullName('Jon Snow');
    await signupPage.inputEmail(randomEmail);
    await signupPage.inputPassword('Password123!');
    await signupPage.inputConfirmPassword('Password123!');
    await signupPage.checkAgreeTerms();
    await signupPage.clickSignUpButton();
    await page.waitForSelector(`//a[contains(text(),'${randomEmail}')]`);
    const emailLink = await page.$(`//a[contains(text(),'${randomEmail}')]`);
    expect(emailLink).not.toBeNull();
    const verifyEmailHeader = await page.$(`//h1[contains(text(),'Verify your email')]`);
    expect(verifyEmailHeader!).toBeTruthy();
    const currentUrl = page.url();
    expect(currentUrl).toContain('https://rabata.io/verify/info/');
  });

  test('Privacy policy', async ({ page }) => {
    const rabataMain = new RabataMain(page);
    const rabataPrivacy= new PrivacyPolicy(page);
    await rabataMain.open();
    await page.waitForLoadState('domcontentloaded');
    await page.waitForLoadState('networkidle');
    await rabataMain.clickPrivacyPolicy();
    const privacyPolicyText1 = await rabataPrivacy.getPrivacyPolicyText1();
    const privacyPolicyText2 = await rabataPrivacy.getPrivacyPolicyText2();
    const privacyPolicyText3 = await rabataPrivacy.getPrivacyPolicyText3();
    expect(privacyPolicyText1).toContain(rabataPrivacy.privacyPolicyText1);
    expect(privacyPolicyText2).toContain(rabataPrivacy.privacyPolicyText2);
    expect(privacyPolicyText3).toContain(rabataPrivacy.privacyPolicyText3);
    });
    
    test('Calculator- default', async ({ page }) => {   //test fails on 133th step of the loop, perhaps because of anti-ddos protection
      const rabataMain = new RabataMain(page);
      await rabataMain.open();
      await page.getByRole('banner').getByRole('link', { name: 'Calculator' }).click();
      
      for (let j = 1; j <= 10; j++) {//"j" approach 10 for clarity, to prevent the test from failing because of anti-ddos protection. Ideally, "j" should approach 1000.
        await page.locator('#dataDownloadInput').fill(j.toString());
    
        for (let i = 1; i <= 10; i++) { //"i" approach 10 for clarity, to prevent the test from failing because of anti-ddos protection. Ideally, "i" should approach 1000.
            await page.locator('#dataApiStoredInput').fill(i.toString());
    
            //get actual values from the graphs 
            const elementRabata = await page.$("#rabataMobileApi");
            const elementAzure = await page.$("#azureMobileApi");
            const elementAmazon = await page.$("#amazonMobileApi");
            const elementGoogle = await page.$("#googleMobileApi");
            //parsing actual values
            const priceRabataActual = isNaN(parseFloat((await elementRabata?.innerText()).replace('$', '').replace(' / yr', '').trim())) ? 'N/A' : parseFloat((await elementRabata?.innerText()).replace('$', '').replace(' / yr', '').trim());
            const priceAzureActual = isNaN(parseFloat((await elementAzure?.innerText()).replace('$', '').replace(' / yr', '').trim())) ? 'N/A' : parseFloat((await elementAzure?.innerText()).replace('$', '').replace(' / yr', '').trim());
            const priceAmazonActual = isNaN(parseFloat((await elementAmazon?.innerText()).replace('$', '').replace(' / yr', '').trim())) ? 'N/A' : parseFloat((await elementAmazon?.innerText()).replace('$', '').replace(' / yr', '').trim());
            const priceGoogleActual = isNaN(parseFloat((await elementGoogle?.innerText()).replace('$', '').replace(' / yr', '').trim())) ? 'N/A' : parseFloat((await elementGoogle?.innerText()).replace('$', '').replace(' / yr', '').trim());
    
            //calculating actual values by formula
            const expectedValues = calculateExpectedValue(i, j);
      
            console.log(`Total Data Stored: ${i}, Monthly Downloaded Data: ${j}, Actual - Rabata: ${priceRabataActual}, Expected - Rabata: ${expectedValues.rabataExpected}`);
            console.log(`Total Data Stored: ${i}, Monthly Downloaded Data: ${j}, Actual - Azure: ${priceAzureActual}, Expected - Azure: ${expectedValues.azureExpected}`);
            console.log(`Total Data Stored: ${i}, Monthly Downloaded Data: ${j}, Actual - Amazon: ${priceAmazonActual}, Expected - Amazon: ${expectedValues.amazonExpected}`);
            console.log(`Total Data Stored: ${i}, Monthly Downloaded Data: ${j}, Actual - Google: ${priceGoogleActual}, Expected - Google: ${expectedValues.googleExpected}`);
    
            //checking are expected values equals to actual
            if (
                priceRabataActual === expectedValues.rabataExpected &&
                priceAzureActual === expectedValues.azureExpected &&
                priceAmazonActual === expectedValues.amazonExpected &&
                priceGoogleActual === expectedValues.googleExpected
            ) {
                console.log(`Values of Total Data Stored = ${i}, j=${j} equals to expected`);
            } else {
              throw new Error(`Values of Total Data Stored = ${i}, j=${j} NOT equals to expected`); //test fails when Actual and Expected values aren't equal
            }
        }
      }
    });
    //Formula
    const calculateExpectedValue = (i, j) => {
      const rabataExpected = 180 * i + 180 * j;
      const azureExpected = 252 * i + 252 * j;
      const amazonExpected = 300 * i + 300 * j;
      const googleExpected = 372 * i + 372 * j;
      return { rabataExpected, azureExpected, amazonExpected, googleExpected };
    }; 

    test('Calculator - Backup', async ({ page }) => {   //test fails on 133th step, perhaps because of anti-ddos protection
      const rabataMain = new RabataMain(page);
      await rabataMain.open();
      await page.getByRole('banner').getByRole('link', { name: 'Calculator' }).click();
      await page.getByText('$59 S3 compatible hot-backup for $59 per 10 TB of storage. Backup').click();
      await page.locator('#dataStoredInput').fill('1');
  
      for (let i = 1; i <= 120; i++) {
          await page.locator('#dataStoredInput').fill(i.toString());
          //Get actual values from the graphs 
          const elementRabata = await page.$("#rabataMobile");
          const elementAzure = await page.$("#azureMobile");
          const elementAmazon = await page.$("#amazonMobile");
          const elementGoogle = await page.$("#googleMobile");
  
          // Parsing actual values
          const priceRabataActual = parseFloat((await elementRabata?.innerText()).replace('$', '').replace(' / yr', '').trim());
          const priceAzureActual = parseFloat((await elementAzure?.innerText()).replace('$', '').replace(' / yr', '').trim());
          const priceAmazonActual = parseFloat((await elementAmazon?.innerText()).replace('$', '').replace(' / yr', '').trim());
          const priceGoogleActual = parseFloat((await elementGoogle?.innerText()).replace('$', '').replace(' / yr', '').trim());
  
          // Calculating expected values
          const expectedValues = calculateExpectedValueBackup(i);
  
          console.log(`Total Data Stored: ${i}, Actual - Rabata: ${priceRabataActual}, Expected - Rabata: ${expectedValues[i].rabataExpected}`);
          console.log(`Total Data Stored: ${i}, Actual - Azure: ${priceAzureActual}, Expected - Azure: ${expectedValues[i].azureExpected}`);
          console.log(`Total Data Stored: ${i}, Actual - Amazon: ${priceAmazonActual}, Expected - Amazon: ${expectedValues[i].amazonExpected}`);
          console.log(`Total Data Stored: ${i}, Actual - Google: ${priceGoogleActual}, Expected - Google: ${expectedValues[i].googleExpected}`);
          
  
        if (
          priceRabataActual === expectedValues[i].rabataExpected &&
          priceAzureActual === expectedValues[i].azureExpected &&
          priceAmazonActual === expectedValues[i].amazonExpected &&
          priceGoogleActual === expectedValues[i].googleExpected
) {
  console.log(`Values of Total Data Stored = ${i}, equals to expected`);
} else {
  throw new Error(`Values of Total Data Stored = ${i}, NOT equals to expected`); // Test fails when actual and expected values aren't equal
}

      }
  });
  
  const calculateExpectedValueBackup = (i) => {
    const incrementActualRabata = 708;
    const incrementActualAzure = 2496;
    const incrementActualAmazon = 3120;
    const incrementActualGoogle = 2760;
    const incrementTotalDataStored = 10;

    let expectedValues = {};

    for (let j = 1; j <= i; j++) {
        const currentActualRabata = incrementActualRabata + Math.floor((j - 1) / incrementTotalDataStored) * incrementActualRabata;
        const currentActualAzure = incrementActualAzure + Math.floor((j - 1) / incrementTotalDataStored) * incrementActualAzure;
        const currentActualAmazon = incrementActualAmazon + Math.floor((j - 1) / incrementTotalDataStored) * incrementActualAmazon; 
        const currentActualGoogle =incrementActualGoogle + Math.floor((j - 1) / incrementTotalDataStored) * incrementActualGoogle; 
        expectedValues[j] = { rabataExpected: currentActualRabata, azureExpected: currentActualAzure, amazonExpected: currentActualAmazon, googleExpected: currentActualGoogle };
    }

    return expectedValues;
};


});

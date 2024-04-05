import { Page } from 'playwright';

export class PrivacyPolicy {
    private page: Page;
    privacyPolicyText1: string;
    privacyPolicyText2: string;
    privacyPolicyText3: string;
    privacyPolicyElement1: string;
    privacyPolicyElement2: string;
    privacyPolicyElement3: string;

    constructor(page: Page) {
        this.page = page;
        this.privacyPolicyText1 = "This Privacy Policy (the “Policy”) describes how the Rabata Technologies LLC (US) & Rabata Technologies LP (EU) (for more details, see “Contact Information” below) (“Rabata,” “we,” “our” or “us”) collect, use, and share information in connection with your use of our websites (the “Sites”), as well as any products, services, and/or applications available on or through the Sites (collectively, the “Services”). However, this Policy does not apply to information customers or users (“users”, “you,” or “your”) may process when using our Services."; 
        this.privacyPolicyText2 = "The information we collect includes “personal data,” which is any information about an identifiable individual, as further set forth in this Policy. Rabata is the sole owner of the information collected on the Sites or through your use of the Services. We will not sell, share, or rent this information to others in ways different from what is disclosed in this Policy."
        this.privacyPolicyText3 = "Further, Rabata respects your privacy and is committed to protecting your personal data in line with the General Data Protection Regulation – Regulation (EU) 2016/679 (“GDPR”). This Policy will inform you as to how we will look after your personal data when you interact with us, including visiting our Sites. It also tells you about your rights in relation to your personal data. We recommend that you read this Policy in full to ensure you are fully informed regarding our privacy practices. If you have any questions about this Policy or Rabata’s data collection, use, and disclosure practices, please contact us at support@rabata.io."
        this.privacyPolicyElement1="//body/div[@id='modalPrivacy']/div[1]/div[3]/div[1]"
        this.privacyPolicyElement2="//body/div[@id='modalPrivacy']/div[1]/div[3]/div[2]"
        this.privacyPolicyElement3="//body/div[@id='modalPrivacy']/div[1]/div[3]/div[3]"
    }

    async getPrivacyPolicyText1(): Promise<string> {
        const element = await this.page.waitForSelector(this.privacyPolicyElement1);
        return element.innerText();
    }

    async getPrivacyPolicyText2(): Promise<string> {
        const element = await this.page.waitForSelector(this.privacyPolicyElement2);
        return element.innerText();
    }

    async getPrivacyPolicyText3(): Promise<string> {
        const element = await this.page.waitForSelector(this.privacyPolicyElement3);
        return element.innerText();
    }
    
   
}
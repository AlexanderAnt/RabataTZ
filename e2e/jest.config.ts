module.exports = {
    // Другие настройки Jest
    reporters: [
      'default',
      ['@wdio/allure-reporter', {
        outputDir: './allure-results',
        disableWebdriverStepsReporting: true,
        disableWebdriverScreenshotsReporting: false,
      }],
    ],
  };
  
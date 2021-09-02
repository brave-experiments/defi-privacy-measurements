const puppeteerExtraLib = require('puppeteer-extra')
const puppeteerExtraPluginStealthLib = require('puppeteer-extra-plugin-stealth')
puppeteerExtraLib.use(puppeteerExtraPluginStealthLib())

const launch = async args => {
  const puppeteerArgs = {
    defaultViewport: null,
    args: [],
    executablePath: args.executablePath,
    headless: args.headless
  }

  if (args.profilePath) {
    puppeteerArgs.args.push(`--user-data-dir=${args.profilePath}`)
  }

  if (args.extraArgs) {
    puppeteerArgs.args.push(...args.extraArgs)
  }

  return await puppeteerExtraLib.launch(puppeteerArgs)
}

module.exports = {
  launch
}

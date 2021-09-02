#!/usr/bin/env node
const argparseLib = require('argparse')

const braveCrawlLib = require('./brave/crawl.js')
const braveLoggerLib = require('./brave/logging.js')
const braveValidateLib = require('./brave/validate.js')

const defaultDebugSetting = 'none'
const defaultCrawlSecs = 30

const parser = new argparseLib.ArgumentParser({
  add_help: true,
  description: 'CLI tool for recording requests made when visiting a URL.'
})
parser.add_argument('-b', '--binary', {
  required: true,
  help: 'Path to a puppeteer compatible browser.'
})
parser.add_argument('--debug', {
  help: `Print debugging information. Default: ${defaultDebugSetting}.`,
  choices: ['none', 'debug', 'verbose'],
  default: defaultDebugSetting
})
parser.add_argument('-u', '--url', {
  help: 'The URL to record requests no',
  required: true
})
parser.add_argument('-p', '--profile', {
  help: 'Path to use and store profile data to.',
  required: false
})
parser.add_argument('-a', '--ancestors', {
  help: 'Log each requests frame hierarchy, not just the immediate parent. ' +
        '(frame URLs are recorded from immediate frame to top most frame)',
  action: 'store_true'
})
parser.add_argument('--interactive', {
  help: 'Show the browser when recording (by default runs headless).',
  action: 'store_true'
})
parser.add_argument('-t', '--secs', {
  help: `The dwell time in seconds. Defaults: ${defaultCrawlSecs} sec.`,
  type: 'int',
  default: defaultCrawlSecs
})
parser.add_argument('-m', '--metamask', {
  help: 'Path to the MetaMask extension.',
  required: false
})

const rawArgs = parser.parse_args()
const [isValid, errorOrArgs] = braveValidateLib.validate(rawArgs)
if (!isValid) {
  throw errorOrArgs
}

(async _ => {
  const logger = braveLoggerLib.getLoggerForLevel(errorOrArgs.debugLevel)
  logger.debug('Executing with arguments: ', errorOrArgs)
  const crawlLog = await braveCrawlLib.crawl(errorOrArgs)
  console.log(JSON.stringify(crawlLog))
  process.exit(crawlLog.success === true ? 0 : 1)
})()

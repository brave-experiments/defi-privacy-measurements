const braveLoggerLib = require('./logging.js')
const bravePuppeteerLib = require('./puppeteer.js')

const onRequest = async (logger, requestLog, request) => {
  let frameUrl, frameId, frameParentId

  const frame = request.frame()

  if (frame) {
    frameUrl = frame.url()
    frameId = frame.id
    frameParentId = frame.parentFrame()?.id
  }

  const requestUrl = request.url()
  const requestType = request.resourceType()

  requestLog.requests.push({
    frameId,
    frameParentId,
    frameUrl,
    url: requestUrl,
    type: requestType
  })

  const numRequests = requestLog.requests.length
  logger.debug(`Request ${numRequests}: ${requestUrl}`)
}

const onTargetCreated = async (logger, requestLog, target) => {
  if (target.type() !== 'page') {
    return
  }
  const page = await target.page()
  page.on('request', onRequest.bind(undefined, logger, requestLog))

  logger.debug('Completed configuring new page.')
}

const crawl = async args => {
  const logger = braveLoggerLib.getLoggerForLevel(args.debugLevel)

  const url = args.url

  const log = Object.create(null)
  log.url = url
  log.arguments = args
  log.timestamp = Date.now()
  log.requests = []
  log.success = true

  let browser
  try {
    browser = await bravePuppeteerLib.launch(args)
    browser.on('targetcreated', onTargetCreated.bind(undefined, logger, log))
    const page = await browser.newPage()

    logger.debug(`Visiting ${url}`)
    await page.goto(url, {})

    const waitTimeMs = args.secs * 1000
    logger.debug(`Waiting for ${waitTimeMs}ms`)
    await page.waitForTimeout(waitTimeMs)
    await page.close()
  } catch (error) {
    log.success = false
    log.msg = error.toString()
    logger.debug(`Caught error when crawling: for ${log.msg}`)
  }

  try {
    logger.debug('Trying to shutdown')
    await browser.close()
  } catch (e) {
    logger.debug(`Error when shutting down: ${e.toString()}`)
  }
  return log
}

module.exports = {
  crawl
}

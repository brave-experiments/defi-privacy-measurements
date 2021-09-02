const fsLib = require('fs')
const urlLib = require('url')

const isUrl = possibleUrl => {
  try {
    (new urlLib.URL(possibleUrl))  // eslint-disable-line
    return true
  } catch (_) {
    return false
  }
}

const isFile = path => {
  return fsLib.existsSync(path) && fsLib.lstatSync(path).isFile()
}

const validate = rawArgs => {
  if (!isFile(rawArgs.binary)) {
    return [false, `Invalid path to Brave binary: ${rawArgs.binary}`]
  }
  const executablePath = rawArgs.binary

  if (!isUrl(rawArgs.url)) {
    return [false, `Found invalid URL: ${rawArgs.url}`]
  }

  const validatedArgs = {
    printFrameHierarchy: !!rawArgs.ancestors,
    debugLevel: rawArgs.debug,
    headless: !rawArgs.interactive,
    profilePath: rawArgs.profile,
    secs: rawArgs.secs,
    url: rawArgs.url,
    metamaskPath: rawArgs.metamask,
    executablePath
  }
  return [true, Object.freeze(validatedArgs)]
}

module.exports = {
  isFile,
  isUrl,
  validate
}

# DeFi Privacy Measurements

This repository contains the code and data that we developed as part of our
research project on privacy and security issues in decentralized finance (DeFi).
You can find our [technical report on arXiv.org](https://arxiv.org/abs/2109.06836).

## Code

* [request-logger/](request-logger): A
  [Puppeteer](https://github.com/puppeteer/puppeteer)-based crawler that takes
  as input a list of URLs that are visited one after another while logging all
  requests that the respective sites make.
* [metamask-patch/](metamask-patch): A proof-of-concept patch for the
  [MetaMask](https://github.com/MetaMask/metamask-extension) wallet which
  replaces the user's real Ethereum address with derived, site-specific
  addresses, to make it harder for DeFi sites and trackers to track the user
  across sites.
* [analysis-scripts/](analysis-scripts): A set of Python scripts that analyze
  the data produced by the request-logger.

## Data

* [data/](data): A set of JSON files that we collected with the help of the
  request-logger.

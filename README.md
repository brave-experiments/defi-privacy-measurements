# DeFi Privacy Measurements

To use DeFi sites like app.uniswap.org, users must connect their Ethereum wallet, allowing the site to create transactions and let the user sign off. Once the user’s wallet is connected, the DeFi site can access the user’s Ethereum address, which is not strictly necessary to craft transactions (e.g. swapping tokens on Uniswap) and it can also lead to (un)intentional leaks of the user’s Ethereum address to third parties.

This repository contains the code to crawl DeFi sites to collect information about ethereum wallet leakage.


# Running the crawler

`node crawler.js <filename>`

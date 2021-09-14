Disclaimer
----------

Note that this patch is a simple proof-of-concept and *not* meant to be used in
production!  It uses hard-coded addresses, will not work for you, and you may
lose funds.

Installation
------------

This patch should cleanly apply on top of MetaMask's v10.1.0 tag.  To apply the
patch, run the following:

    git clone https://github.com/MetaMask/metamask-extension.git
    cd metamask-extension/
    cp /path/to/0001-Use-site-specific-derived-Ethereum-addresses.patch .
    git checkout v10.1.0
    git apply 0001-Use-site-specific-derived-Ethereum-addresses.patch

Afterwards, proceed to build and install MetaMask.

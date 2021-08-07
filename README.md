```
usage: run.js [-h] -b BINARY [--debug {none,debug,verbose}] -u URL
              [-p PROFILE] [--interactive] [-t SECS]

CLI tool for recording requests made when visiting a URL.

optional arguments:
  -h, --help            show this help message and exit
  -b BINARY, --binary BINARY
                        Path to a puppeteer compatible browser.
  --debug {none,debug,verbose}
                        Print debugging information. Default: none.
  -u URL, --url URL     The URL to record requests no
  -p PROFILE, --profile PROFILE
                        Path to use and store profile data to.
  --interactive         Show the browser when recording (by default runs
                        headless).
  -t SECS, --secs SECS  The dwell time in seconds. Defaults: 30 sec.
```

const csv = require('csv-parser');
const fs = require('fs');
const request_client = require('request-promise-native');

// Read the list of sites to crawl  
/*let sites = [];
fs.createReadStream('sites.csv')
  .pipe(csv())
  .on('data', (row) => {
  sites.push(row['site']);
  console.log(row['site']);
  })
  .on('end', () => {
    console.log('sites.csv processed');
   });
  console.log(sites);
  evaluatePage: () => ({
      title: $('title').text(),
    }),
    onSuccess: result => {
      console.log(`Got ${result.result.title} for ${result.options.url}.`);
    },
  });
  
*/
 // Crawl the site

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  const result = [];

  await page.setRequestInterception(true);

  page.on('request', request => {
    request_client({
      uri: request.url(),
      resolveWithFullResponse: true,
    }).then(response => {
      const request_url = request.url();
      const request_headers = request.headers();
      const request_post_data = request.postData();
      const response_headers = response.headers;
      const response_size = response_headers['content-length'];
      const response_body = response.body;

      result.push({
        request_url,
        request_headers,
        request_post_data,
        response_headers,
        response_size,
        response_body,
      });

      console.log(result);
      request.continue();
    }).catch(error => {
      console.error(error);
      request.abort();
    });
  });

  await page.goto('https://app.sushi.com', {
    waitUntil: 'networkidle0',
  });

  await browser.close();
})();

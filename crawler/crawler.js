const HCCrawler = require('headless-chrome-crawler');
const request_client = require('request-promise-native');

(async () => {
  const crawler = await HCCrawler.launch({
    maxDepth: 3,
    customCrawl: async (page, crawl) => {
      // You can access the page object before requests
      const csv = [];
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

      csv.push({
        request_url,
        request_headers,
        request_post_data,
        response_headers,
        response_size,
        response_body,
      });

      console.log(csv);
      request.continue();
    }).catch(error => {
      console.error(error);
      request.abort();
    });
  }); 
      // The result contains options, links, cookies and etc.
      const result = await crawl();
      // You can access the page object after requests
      result.content = await page.content();
      // You need to extend and return the crawled result
      return result;
    },
    onSuccess: result => {
      console.log(`Got ${result.content} for ${result.options.url}.`);
    },
  });
  await crawler.queue('https://app.sushi.com/');
  await crawler.onIdle();
  await crawler.close();
})();

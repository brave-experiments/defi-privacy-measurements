const HCCrawler = require('headless-chrome-crawler');
const request_client = require('request-promise-native');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;

var filename = process.argv.slice(2)[0];
const FILE = filename;
console.log(FILE);

const csvWriter = createCsvWriter({
	path: FILE,
	header: [
		{id: 'defi_url', title: 'defi_url'},
		{id: 'request_url', title: 'request_url'},
		{id: 'request_headers', title: 'request_headers'},
		{id: 'request_post_data', title: 'request_post_data'},
		{id: 'response_headers', title: 'response_headers'},
		{id: 'response_body', title: 'response_body'}
	]
});

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
      const response_body = response.body;
	
      const url = page.url();
      csvWriter.writeRecords([{defi_url: url, 
                              request_url: request_url, 
                              request_headers: request_headers, 
                              request_post_data: request_post_data, 
                              response_headers: response_headers,
                              response_body: response_body}]);

	//console.log(csv);
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

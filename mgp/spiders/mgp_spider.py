from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector

from mgp.items import MgpAuthor

from urlparse import urlparse, parse_qs

class MgpSpider(CrawlSpider):
    name = 'mgp'
    allowed_domains = ['www.genealogy.ams.org']
    start_urls = ['http://www.genealogy.ams.org/id.php?id=171963']
    rules = [Rule(SgmlLinkExtractor(allow=['id\.php\?id=\d+']),
                  callback='parse_author',
                  follow=True)]

    def parse_author(self, response):
        sel = Selector(response)
        author = MgpAuthor()
        author['url'] = response.url
        author['name'] = sel.xpath("//div[@id='paddingWrapper']/h2[1]/text()").extract()[0].strip()
        author['advisors'] = sel.xpath("//div[@id='paddingWrapper']/p[2]/a/text()").extract()
        author['mgpid'] = int(parse_qs(urlparse(response.url)[4])['id'][0])
        return author

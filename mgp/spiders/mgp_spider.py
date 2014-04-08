import itertools
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spider import Spider
from urlparse import urlparse, parse_qs, urljoin

from mgp.items import MgpAuthor

def int_or_none(value):
    try:
        return int(value)
    except ValueError:
        return None

class MgpSpider(Spider):
    name = 'mgp'
    allowed_domains = ['www.genealogy.ams.org']
    start_urls = ['http://www.genealogy.ams.org/id.php?id=171963']

    def parse(self, response):
        sel = Selector(response)
        author = MgpAuthor()
        author['url'] = response.url
        author['mgpid'] = int(parse_qs(urlparse(response.url)[4])['id'][0])
        author['name'] = sel.xpath("//div[@id='paddingWrapper']/h2[1]/text()").extract()[0].strip()
        author['year'] = int_or_none(sel.xpath("//div[@id='paddingWrapper']/div[2]/span/text()[2]").extract()[0])
        advisor_a = sel.xpath("//div[@id='paddingWrapper']/p[2]/a")
        author['advisors'] = advisor_a.xpath("./text()").extract()
        advisor_links = advisor_a.xpath('./@href').extract()
        return itertools.chain([author], (Request(urljoin(response.url,link)) for link in advisor_links))

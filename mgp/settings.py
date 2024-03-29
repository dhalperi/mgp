# Scrapy settings for mgp project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'mgp'

SPIDER_MODULES = ['mgp.spiders']
NEWSPIDER_MODULE = 'mgp.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'mgp (+http://www.halper.in)'

# Limit to depth 2 for testing
DEPTH_LIMIT = 2

DOWNLOAD_DELAY = 0.25

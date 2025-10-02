import scrapy, yaml
from harvester.items import ArticleItem

class ForumRssSpider(scrapy.Spider):
    name = "forum_rss"
    domain_category = "Forums"
    custom_settings = {"ROBOTSTXT_OBEY": True}

    def start_requests(self):
        with open("configs/sources_forums.yml", "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}
        for url in (cfg.get("rss_feeds") or []):
            yield scrapy.Request(url, callback=self.parse_feed)

    def parse_feed(self, response):
        for link in response.xpath("//item/link/text()").getall():
            yield scrapy.Request(link, callback=self.parse_thread)

    def parse_thread(self, response):
        title = response.xpath("//title/text()").get() or response.css("title::text").get() or ""
        html = response.text
        yield ArticleItem(url=response.url, title=title, html=html)

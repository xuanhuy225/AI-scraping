import scrapy
import yaml
from harvester.items import ArticleItem

class RssSpider(scrapy.Spider):
    name = "news_rss"
    custom_settings = {"ROBOTSTXT_OBEY": True}
    domain_category = "News"

    def start_requests(self):
        # Load feeds from configs/sources_news.yml
        with open("configs/sources_news.yml", "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        feeds = cfg.get("rss_feeds", [])
        for url in feeds:
            yield scrapy.Request(url, callback=self.parse_feed)

    def parse_feed(self, response):
        for link in response.xpath("//item/link/text()").getall():
            yield scrapy.Request(link, callback=self.parse_article)

    def parse_article(self, response):
        title = response.xpath("//title/text()").get() or response.css("title::text").get() or ""
        html = response.text
        yield ArticleItem(url=response.url, title=title, html=html)

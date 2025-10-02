import scrapy, yaml
from harvester.items import ArticleItem

class BooksSpider(scrapy.Spider):
    name = "books"
    domain_category = "Books"
    custom_settings = {"ROBOTSTXT_OBEY": True}

    def start_requests(self):
        with open("configs/sources_books.yml", "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}
        for url in (cfg.get("rss_feeds") or []):
            yield scrapy.Request(url, callback=self.parse_feed)
        for sm in (cfg.get("sitemaps") or []):
            yield scrapy.Request(sm, callback=self.parse_sitemap)

    def parse_feed(self, response):
        for link in response.xpath("//item/link/text()").getall():
            yield scrapy.Request(link, callback=self.parse_book_page)

    def parse_sitemap(self, response):
        for link in response.xpath("//*[local-name()='loc']/text()").getall():
            yield scrapy.Request(link, callback=self.parse_book_page)

    def parse_book_page(self, response):
        title = response.xpath("//title/text()").get() or response.css("title::text").get() or ""
        html = response.text
        yield ArticleItem(url=response.url, title=title, html=html)

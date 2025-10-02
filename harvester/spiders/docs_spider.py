import yaml
from scrapy.spiders import SitemapSpider
from harvester.items import ArticleItem

class DocsSitemapSpider(SitemapSpider):
    name = "docs_sitemap"
    domain_category = "Technical Documents"
    custom_settings = {"ROBOTSTXT_OBEY": True}

    def start_requests(self):
        with open("configs/sources_docs.yml", "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}
        self.sitemap_urls = cfg.get("sitemaps") or []
        self.allow_paths = cfg.get("allow_paths") or []
        return super().start_requests()

    def sitemap_filter(self, entries):
        for entry in entries:
            loc = entry.get('loc') or ""
            if not self.allow_paths:
                yield entry
            else:
                if any(loc.startswith(pfx) or (pfx in loc) for pfx in self.allow_paths):
                    yield entry

    def parse(self, response):
        title = response.xpath("//title/text()").get() or response.css("title::text").get() or ""
        html = response.text
        yield ArticleItem(url=response.url, title=title, html=html)

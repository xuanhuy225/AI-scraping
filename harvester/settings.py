BOT_NAME = "harvester"
SPIDER_MODULES = ["harvester.spiders"]
NEWSPIDER_MODULE = "harvester.spiders"

ROBOTSTXT_OBEY = True
CONCURRENT_REQUESTS = 8
DOWNLOAD_DELAY = 0.5

ITEM_PIPELINES = {
    "harvester.pipelines.CleanAndWritePipeline": 300,
}

FEED_EXPORT_ENCODING = "utf-8"

DOWNLOADER_MIDDLEWARES = {
    "scrapy_playwright.middleware.ScrapyPlaywrightDownloaderMiddleware": 543,
}
PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 30000
PLAYWRIGHT_LAUNCH_OPTIONS = {"headless": True}

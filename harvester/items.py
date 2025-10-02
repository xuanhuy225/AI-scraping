import scrapy

class ArticleItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    html = scrapy.Field()      # raw html sample
    content = scrapy.Field()   # (reserved) raw extracted content if used
    images = scrapy.Field()    # (reserved) list of images
    lang = scrapy.Field()      # (reserved)

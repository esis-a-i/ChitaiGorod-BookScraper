import scrapy
from scrapy.spiders import SitemapSpider
import re
from ..items import BookItem

class ChitaiGorodSpider(SitemapSpider):
    name = 'book_spider'
    sitemap_urls = ['https://www.chitai-gorod.ru/sitemap/authors1.xml']

    def parse(self, response):
        book_links = response.xpath('//div[@class="products-list"]/article/a/@href').getall()
        yield from response.follow_all(book_links, self.parse_book)
        
        next_page = response.xpath('//a[@rel="next"]/@href').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_book(self, response):
        item = BookItem()
        
        price_text = response.xpath('//span[contains(@class, "product-offer-price")]/text()').get('')
        price = re.sub(r'[^0-9.]', '', price_text.split('₽')[0].strip())
        currency = '₽' if '₽' in price_text else ''

        style = response.xpath('//button[contains(@style, "background-image")]/@style').get('')
        image_url = re.search(r'url\((.*?)\)', style).group(1) if style else ''

        item['title'] = response.xpath('//h1/text()').get('').strip()
        authors = response.xpath('//ul[@class="product-authors"]/li/a/text()').getall()
        item['author'] = ', '.join(authors) if authors else None
        item['description'] = ' '.join(response.xpath('//div[contains(@class, "product-description-short")]/text()').getall()).strip() or None
        item['price_amount'] = float(price) if price else None
        item['price_currency'] = currency or None
        
        rating_value = response.xpath('//span[@itemprop="ratingValue"]/text()').get('')
        item['rating_value'] = float(rating_value) if rating_value else None
        
        rating_count = response.xpath('//span[@itemprop="ratingCount"]/text()').get('')
        if rating_count:
            rating_count_clean = re.sub(r'[^\d]', '', rating_count)
            item['rating_count'] = int(rating_count_clean) if rating_count_clean else None
        else:
            item['rating_count'] = None
        
        pub_year = response.xpath('//span[@itemprop="datePublished"]/span/text()').get('').strip()
        item['publication_year'] = int(pub_year) if pub_year else None
        
        item['isbn'] = response.xpath('//span[@itemprop="isbn"]/span/text()').get('').strip()
        
        pages = response.xpath('//span[@itemprop="numberOfPages"]/span/text()').get('').strip()
        item['pages_cnt'] = int(pages) if pages else None
        
        item['publisher'] = response.xpath('//span[@itemprop="publisher"]/a/text()').get('').strip() or None
        item['book_cover'] = image_url or None
        item['source_url'] = response.url

        yield item
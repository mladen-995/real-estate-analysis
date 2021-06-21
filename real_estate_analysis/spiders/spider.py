import scrapy
from ..items import RealEstateItem



class CustomSpider(scrapy.Spider):
    name = 'custom_spider'

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES' : {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
        },
        'MYSQL_HOST': 'localhost',
        'MYSQL_USERNAME': 'mladen',
        'MYSQL_PASSWORD': 'password',
        'MYSQL_DATABASE': 'crawler',
    }


    def start_requests(self):
        yield scrapy.Request('https://www.nekretnine.rs/stambeni-objekti/stanovi/cena/1_50000/lista/po-stranici/20/', self.parseIndex)
        yield scrapy.Request('https://www.nekretnine.rs/stambeni-objekti/stanovi/cena/50001_100000/lista/po-stranici/20/', self.parseIndex)
        yield scrapy.Request('https://www.nekretnine.rs/stambeni-objekti/stanovi/cena/100001_1000000/lista/po-stranici/20/', self.parseIndex)
        
        
        yield scrapy.Request('https://www.nekretnine.rs/stambeni-objekti/kuce/lista/po-stranici/10/', self.parseIndex)


    def parseIndex(self, response):
        next_link = response.css('.next-article-button::attr(href)')
        links = []
        for offer in response.css('.advert-list .offer'):
            links.append('https://www.nekretnine.rs' + str(offer.css('h2 a::attr(href)').get()))

        for link in links:
            yield scrapy.Request(link)

        yield scrapy.Request('https://www.nekretnine.rs' + str(next_link.get()), self.parseIndex)

    def parseDetail(self, type, details):
        for detail in details:
            if type in detail.get():
                return detail.css('strong ::text').get().strip()

    def parse(self, response):
        details = response.css('.property__amenities:nth-child(2) ul li')


        real_estate_item = RealEstateItem()
        real_estate_item['url'] = response.url
        real_estate_item['type'] = self.parseDetail('Transakcija', details)
        real_estate_item['offer_type'] = response.css('ol.breadcrumb li.breadcrumb-item:nth-child(3) a::attr(title)').get()
        real_estate_item['area'] = self.parseDetail('Kvadratura', details)
        real_estate_item['number_of_rooms'] = self.parseDetail('Ukupan broj soba', details)
        real_estate_item['level'] = self.parseDetail('Spratnost', details)
        real_estate_item['total_level'] = self.parseDetail('Ukupan broj spratova', details)
        real_estate_item['number_of_toilets'] = self.parseDetail('Broj kupatila', details)
        real_estate_item['build_year'] = self.parseDetail('Godina izgradnje', details)

        fetchedField = self.parseDetail('Površina zemljišta', details)
        if fetchedField:
            fetchedFieldSplited = fetchedField.split(' ')
            if fetchedFieldSplited[1] == 'm²':
                real_estate_item['area_field'] = fetchedFieldSplited[0]
            elif fetchedFieldSplited[1] == 'ar':
                real_estate_item['area_field'] = float(fetchedFieldSplited[0]) * 100

        if self.parseDetail('Uknjiženo', details):
            real_estate_item['registered'] = True

        real_estate_item['price'] = response.css('.stickyBox__price::text').get()
        

        real_estate_item['city'] = response.css('.property__location ul li:nth-child(3)::text').get()
        real_estate_item['city_part'] = response.css('.property__location ul li:nth-child(4)::text').get()
        real_estate_item['address'] = response.css('.property__location ul li:nth-child(5)::text').get()
        

        additional = response.css('.property__amenities:nth-child(3) ul li')
        for additi in additional:
            if 'Lift' in additi.get():
                real_estate_item['has_elevator'] = True
            
            if 'Terasa' in additi.get() or 'Balkon' in additi.get() or 'Lođa' in additi.get():
                real_estate_item['has_balcony'] = True

            if 'Garaža' in additi.get() or 'Garažno mesto' in additi.get() or 'Spoljno parking mesto' in additi.get() or 'Javni parking' in additi.get() or 'Rezervisan parking' in additi.get():
                real_estate_item['has_parking'] = True

        rest = response.css('.property__amenities:nth-child(6) ul li')

        for rr in rest:
            if 'Grejanje' in rr.get():
                real_estate_item['heating_type'] = rr.css('::text').get().split(':')[1].strip()

        yield real_estate_item

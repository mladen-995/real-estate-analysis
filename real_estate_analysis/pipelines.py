# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
from scrapy.exporters import CsvItemExporter
from scrapy.exporters import BaseItemExporter

class PrepareItemPipeline:
    def process_item(self, item, spider):
        item.setdefault('heating_type', None)
        item.setdefault('has_elevator', False)
        item.setdefault('has_balcony', False)
        item.setdefault('area_field', None)
        item.setdefault('has_parking', False)
        item.setdefault('registered', False)
        item.setdefault('price', None)
        item.setdefault('area', None)

        if item['price']:
            item['price'] = float(item['price'].replace('EUR', '').strip().replace(' ', ''))

        if item['area']:
            item['area'] = float(item['area'].replace('m²', '').strip().replace(' ', ''))

        if item['build_year']:
            item['build_year'] = int(item['build_year'])

        if item['area_field']:
            item['area_field'] = float(item['area_field'])

        if item['level']:
            if item['level'] == 'Suteren' or item['level'] == 'Visoko prizemlje':
                item['level'] = 0
            else:
                item['level'] = int(item['level'])

        if item['total_level']:
            item['total_level'] = int(item['total_level'])

        return item

class ExportCSV(BaseItemExporter):
    def open_spider(self, spider):
        self.exx = CsvItemExporter(file=open('test.csv', 'wb'))
        self.exx.start_exporting()

    def close_spider(self, spider):
        self.exx.finish_exporting()
        self.exx.close()

    def process_item(self, item, spider):
        self.exx.export_item(item)
        return item
    


class MySqlPipeline:
    def __init__(self, host, user, password, database) -> None:
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            database=crawler.settings.get('MYSQL_DATABASE'),
        )

    def open_spider(self, spider):
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        self.cursor.execute("INSERT INTO records (url, type, offer_type, city, city_part, address, area, price, build_year, area_field, level, total_level, registered, heating_type, number_of_rooms, number_of_toilets, has_elevator, has_balcony, has_parking) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (
                item['url'],
                item['type'],
                item['offer_type'],
                item['city'],
                item['city_part'],
                item['address'],
                item['area'],
                item['price'],
                item['build_year'],
                item['area_field'],
                item['level'],
                item['total_level'],
                item['registered'],
                item['heating_type'],
                item['number_of_rooms'],
                item['number_of_toilets'],
                item['has_elevator'],
                item['has_balcony'],
                item['has_parking']
            ))

        self.conn.commit()
        return item

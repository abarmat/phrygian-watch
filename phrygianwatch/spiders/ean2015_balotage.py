# -*- coding: utf-8 -*-
import scrapy

from datetime import datetime
from scrapy.loader.processors import TakeFirst
from phrygianwatch.items import TelegramaItem


# Elecciones Argentinas Nacionales (Ballotage) 2015

class EAN2015BallotageSpider(scrapy.Spider):
    name = "ean2015ballotage"
    allowed_domains = ["resultados.gob.ar"]
    start_urls = (
        'http://www.resultados.gob.ar/bltgetelegr/IPRO.htm',
    )

    def parse(self, response):
        for href in response.css('a[target="secciones"]::attr("href")').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse_seccion)

    def parse_seccion(self, response):
        for href in response.css('a[target="circuitos"]::attr("href")').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse_circuito)

    def parse_circuito(self, response):
        for href in response.css('a[target="mesas"]::attr("href")').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse_mesa)
    
    def parse_mesa(self, response):
        for href in response.css('a[target="caja_pdf"]::attr("href")').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse_telegrama)

    def parse_telegrama(self, response):
        # Create item
        item = TelegramaItem()
        tokens = response.url.split('/')

        item['url'] = response.url
        item['pdf'] = item['url'].replace('htm', 'pdf')
        item['mesa'] = response.css('.cabmesa + td::text')[0].extract()
        item['docid'] = tokens[-1].replace('.htm', '')
        item['circuito'] = tokens[-2]
        item['seccion'] = tokens[-3]
        item['provincia'] = tokens[-4]
        item['created_at'] = str(datetime.utcnow())

        item['votos_scioli'] = int(response.css('#TVOTOS tbody tr:nth-child(1) td::text')[0].extract())
        item['votos_macri'] = int(response.css('#TVOTOS tbody tr:nth-child(2) td::text')[0].extract())
        item['votos_nulos'] = int(response.css('.pt1 tbody tr:nth-child(1) td::text')[0].extract())
        item['votos_blancos'] = int(response.css('.pt1 tbody tr:nth-child(2) td::text')[0].extract())
        item['votos_recurridos'] = int(response.css('.pt1 tbody tr:nth-child(3) td::text')[0].extract())
        item['votos_impugnados'] = int(response.css('.pt2 tbody td::text')[0].extract())

        yield item


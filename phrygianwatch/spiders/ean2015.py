# -*- coding: utf-8 -*-
import scrapy

from datetime import datetime
from scrapy.loader.processors import TakeFirst
from phrygianwatch.items import TelegramaItem


# Elecciones Argentinas Nacionales 2015

class EAN2015Spider(scrapy.Spider):
    name = "ean2015"
    allowed_domains = ["resultados.gob.ar"]
    start_urls = (
        'http://www.resultados.gob.ar/nacionaltelegr/IPRO.htm',
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
        for e in response.css('a[target="caja_pdf"]'):
            # Select relevant info
            href = TakeFirst()(e.css('a::attr("href")').extract())
            name = TakeFirst()(e.xpath('text()').extract())
            
            # Create item
            item = TelegramaItem()
            item['url'] = response.urljoin(href)
            item['mesa'] = name

            tokens = item['url'].split('/')            
            item['docid'] = tokens[-1].replace('.htm', '')
            item['circuito'] = tokens[-2]
            item['seccion'] = tokens[-3]
            item['provincia'] = tokens[-4]
            item['created_at'] = str(datetime.utcnow())
            
            yield item

# -*- coding: utf-8 -*-

import scrapy


class TelegramaItem(scrapy.Item):
    url = scrapy.Field()
    docid = scrapy.Field()
    mesa = scrapy.Field()
    circuito = scrapy.Field()
    seccion = scrapy.Field()
    provincia = scrapy.Field()
    created_at = scrapy.Field(serializer=str)

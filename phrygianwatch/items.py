# -*- coding: utf-8 -*-

import scrapy


class TelegramaItem(scrapy.Item):
    docid = scrapy.Field()
    url = scrapy.Field()
    pdf = scrapy.Field()
    mesa = scrapy.Field()
    circuito = scrapy.Field()
    seccion = scrapy.Field()
    provincia = scrapy.Field()
    votos_macri = scrapy.Field()
    votos_scioli = scrapy.Field()
    votos_blancos = scrapy.Field()
    votos_nulos = scrapy.Field()
    votos_recurridos = scrapy.Field()
    votos_impugnados = scrapy.Field()
    created_at = scrapy.Field(serializer=str)

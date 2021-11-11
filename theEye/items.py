# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TheeyeItem(scrapy.Item):
    # define the fields for your item here like:
    nombre = scrapy.Field()
    works = scrapy.Field()
    education = scrapy.Field()
    ciudad_actual = scrapy.Field()
    localidad_natal = scrapy.Field()
    telefono_movil = scrapy.Field()
    facebook = scrapy.Field()
    correo = scrapy.Field()
    fecha_nacimiento = scrapy.Field()
    genero = scrapy.Field()
    situacion_sentimental = scrapy.Field()

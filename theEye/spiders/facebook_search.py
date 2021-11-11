import scrapy
from theEye.items import TheeyeItem
from scrapy.http import FormRequest

class FacebookSearchSpider(scrapy.Spider):

    custom_settings = {
        'FEED_EXPORT_FIELDS': ['nombre', 'ciudad_actual', 'correo', 'education', 'facebook', 'fecha_nacimiento',
                               'genero', 'localidad_natal', 'situacion_sentimental', 'telefono_movil', 'works']
    }

    name = 'facebook_search'
    # allowed_domains = ['https://mbasic.facebook.com']
    start_urls = ['https://mbasic.facebook.com']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.facebook_busqueda = self.facebook_busqueda.replace("_", " ")

    def parse(self, response):

        return FormRequest.from_response(
            response,
            formxpath='//form[contains(@action, "login")]',
            formdata={'email': self.facebook_username, 'pass': self.facebook_password},
            callback=self.parse_home
        )

    def parse_home(self, response):
        # Manejar la redireccion para no establecer el dispositivo de confianza
        if response.xpath("//div/a[contains(@href,'save-device')]"):
            self.logger.info('Going through the "save-device" checkpoint')
            return FormRequest.from_response(
                response,
                formdata={'name_action_selected': 'dont_save'},
                callback=self.parse_home
            )
        # Realizar busqueda en el formulario
        return FormRequest.from_response(
            response,
            formxpath="//form[@action='/search/' and .//input[@placeholder='Busca en Facebook']]",
            formdata={'query': self.facebook_busqueda},
            callback=self.parse_lista_busqueda
        )
        # Buscar dentro del header el enlace a "amigos"
        # amigos_element = response.xpath("//div[@id='header']//a[contains(@href,'friends/center')]")[0]
        # url_home_amigos = response.urljoin(amigos_element.attrib["href"])

        # return scrapy.Request(url_home_amigos, callback=self.parse_amigos_home)

    def parse_lista_busqueda(self, response):
        self.logger.info('parse_lista_busqueda')
        boton_ver_todo = response.xpath("//div[./div/h3/div[contains(text(),'Personas')]]//a[text()='Ver todo']")
        if boton_ver_todo:
            url_boton_ver_todo = response.urljoin(boton_ver_todo.attrib["href"])
            yield scrapy.Request(url_boton_ver_todo, callback=self.parse_lista_perfiles)
        else:
            for perfil_element in response.xpath(
                    "//div[./div/h3/div[contains(text(),'Personas')]]//table//td/a[./div]"):
                url_perfil_element = response.urljoin(perfil_element.attrib["href"])
                yield scrapy.Request(url_perfil_element, callback=self.parse_perfil)
        # bloque_personas = response.xpath("//div[./div/h3/div[contains(text(),'Personas')]]").extract()

    def parse_lista_perfiles(self, response):
        for perfil_element in response.xpath("//div[@id='BrowseResultsContainer']//table//td/a[./div]"):
            url_perfil_element = response.urljoin(perfil_element.attrib["href"])
            yield scrapy.Request(url_perfil_element, callback=self.parse_perfil, priority=10)
        ver_mas_resultados_element = response.xpath("//div[@id='BrowseResultsContainer']//div[@id='see_more_pager']/a")
        if ver_mas_resultados_element:
            url_ver_mas_resultados_element = response.urljoin(ver_mas_resultados_element.attrib["href"])
            yield scrapy.Request(url_ver_mas_resultados_element, callback=self.parse_lista_perfiles)

    def parse_perfil(self, response):
        self.logger.info('parse_perfil')
        nombre = response.xpath("//span/div/span/strong/text()")[0].root
        works = response.xpath("//div[@id='objects_container']//div[@id='work']//a/text()").extract()
        education = response.xpath(
            "//div[@id='objects_container']//div[@id='education']//div/div/div/div/div/div/div/span/text()").extract()
        ciudad_actual = response.xpath(
            "//div[@id='objects_container']//div[@id='living']/div/div/div//table[.//span[contains(text(),'Ciudad actual')]]//td[not(.//span[contains(text(),'Ciudad actual')])]//a/text()").extract()
        localidad_natal = response.xpath(
            "//div[@id='objects_container']//div[@id='living']/div/div/div//table[.//span[contains(text(),'Localidad natal')]]//td[not(.//span[contains(text(),'Localidad natal')])]//a/text()").extract()
        telefono_movil = response.xpath(
            "//div[@id='objects_container']//div[@id='contact-info']/div/div/div//table[.//span[contains(text(),'Móvil')]]//td[not(.//span[contains(text(),'Móvil')])]//span/span/text()").extract()
        facebook = response.xpath(
            "//div[@id='objects_container']//div[@id='contact-info']/div/div/div//table[.//span[contains(text(),'Facebook')]]//td[not(.//span[contains(text(),'Facebook')])]/div/text()").extract()
        correo = response.xpath(
            "//div[@id='objects_container']//div[@id='contact-info']/div/div/div//table[.//span[contains(text(),'Correo')]]//td[not(.//span[contains(text(),'Correo')])]//a/text()").extract()
        fecha_nacimiento = response.xpath(
            "//div[@id='objects_container']//div[@id='basic-info']/div/div/div//table[.//span[contains(text(),'Fecha de nacimiento')]]//td[not(.//span[contains(text(),'Fecha de nacimiento')])]/div/text()").extract()
        genero = response.xpath(
            "//div[@id='objects_container']//div[@id='basic-info']/div/div/div//table[.//span[contains(text(),'Género')]]//td[not(.//span[contains(text(),'Género')])]/div/text()").extract()
        situacion_sentimental = response.xpath(
            "//div[@id='objects_container']//div[@id='relationship']//div/div/div/div/div/text()").extract()
        item = TheeyeItem()
        item['nombre'] = nombre
        item['works'] = works
        item['education'] = education
        item['ciudad_actual'] = ciudad_actual
        item['localidad_natal'] = localidad_natal
        item['telefono_movil'] = telefono_movil
        item['facebook'] = facebook
        item['correo'] = correo
        item['fecha_nacimiento'] = fecha_nacimiento
        item['genero'] = genero
        item['situacion_sentimental'] = situacion_sentimental
        yield item

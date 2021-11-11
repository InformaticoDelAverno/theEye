import scrapy
from scrapy.http import FormRequest
from theEye.items import TheeyeItem


class FacebookFriendsSpider(scrapy.Spider):
    custom_settings = {
        'FEED_EXPORT_FIELDS': ['nombre', 'ciudad_actual', 'correo', 'education', 'facebook', 'fecha_nacimiento',
                               'genero', 'localidad_natal', 'situacion_sentimental', 'telefono_movil', 'works'],
    }

    name = 'facebook_friends'
    # allowed_domains = ['https://mbasic.facebook.com']
    start_urls = ['https://mbasic.facebook.com']

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
        # Buscar dentro del header el enlace a "amigos"
        amigos_element = response.xpath("//div[@id='header']//a[contains(@href,'friends/center')]")[0]
        url_home_amigos = response.urljoin(amigos_element.attrib["href"])

        return scrapy.Request(url_home_amigos, callback=self.parse_amigos_home)

    def parse_amigos_home(self, response):
        amigos_element = \
            response.xpath("//div[@id='friends_center_main']//a[contains(@href,'friends/center/friends')]")[0]
        url_lista_amigos = response.urljoin(amigos_element.attrib["href"])
        return scrapy.Request(url_lista_amigos, callback=self.parse_lista_amigos)

    def parse_lista_amigos(self, response):
        for friend_card in response.xpath("//div[@id='friends_center_main']//table//td//a"):
            friend_profile_url = response.urljoin(friend_card.attrib['href'])
            yield scrapy.Request(friend_profile_url, callback=self.parse_home_friend_profile)
        self.logger.info('parse_lista_amigos')
        # Hacemos la paginacion
        ver_mas_element = response.xpath("//a[./span[contains(text(),'Ver más')]]")
        if ver_mas_element:
            ver_mas_element_url = response.urljoin(ver_mas_element.attrib['href'])
            yield scrapy.Request(ver_mas_element_url, callback=self.parse_lista_amigos)

    def parse_home_friend_profile(self, response):
        # en este enlace se encuentra la foto de perfil (por si se quiere dercargar)
        url_foto_perfil = response.xpath("//img[contains(@alt,'profile picture')]")[0].attrib['src']
        perfil_completo_element = response.xpath("//div[@id='objects_container']//a[.//span[text()='Ver perfil']]")[
            0]
        url_perfil_completo = response.urljoin(perfil_completo_element.attrib["href"])
        yield scrapy.Request(url_perfil_completo, callback=self.parse_friend_profile, priority=5)

    def parse_friend_profile(self, response):
        informacion_element = response.xpath("//div[@id='objects_container']//div/a[text()='Información']")[0]
        url_informacion = response.urljoin(informacion_element.attrib["href"])
        yield scrapy.Request(url_informacion, callback=self.parse_friend_information, priority=10)

    def parse_friend_information(self, response):
        self.logger.info('parse_friend_information')
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

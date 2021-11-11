# -*- coding: utf-8 -*-
# Only for debug
import argparse
import sys
from datetime import datetime

from scrapy import cmdline


def main(user, password, busqueda):

    if busqueda:
        facebook_busqueda = busqueda.replace(" ", "_")
        cmdline.execute(
            f'scrapy crawl facebook_search -o {datetime.now().strftime("%Y%m%d-%H%M%S")}resultados_busqueda.csv -a facebook_username={user} -a facebook_password={password} -a facebook_busqueda={facebook_busqueda}'.split())
    else:
        cmdline.execute(
            f'scrapy crawl facebook_friends -o {datetime.now().strftime("%Y%m%d-%H%M%S")}resultados_friends.csv -a facebook_username={user} -a facebook_password={password}'.split())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            formatter_class=argparse.RawTextHelpFormatter,
            description='''
        theEye es una herramienta que extrae informacion de facebook haciendo uso de tecnicas de scrapping.
        Ofrece dos posibilidades de uso. 
        - Si unicamente especificas un usuario y password, se intentará descargar la informacion de tus amigos.
        - Si además especificas una cadena de busqueda, intentará descargar la informacion de los usuarios que
        el buscador de facebook retorne para dicha cadena. 
        ''',
            usage=f'''main.py [args]''')
    parser.add_argument("--f_user", help="Usuario de facebook")
    parser.add_argument("--f_password", help="Password de facebook")
    parser.add_argument("--f_busqueda", help="Busqueda en facebook")

    args = parser.parse_args(sys.argv[1:])
    if not (args.f_user or args.f_password):
        parser.print_help()
        sys.exit(1)
    main(user=args.f_user, password=args.f_password, busqueda=args.f_busqueda)
    print("--FIN--")



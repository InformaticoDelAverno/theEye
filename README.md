# theEye
theEye es una herramienta que extrae informacion de facebook haciendo uso de tecnicas de scrapping.

Ofrece dos posibilidades de uso. 
- Si unicamente especificas un usuario y password, se intentará descargar la informacion de tus amigos.
- Si además especificas una cadena de busqueda, intentará descargar la informacion de los usuarios que
el buscador de facebook retorne para dicha cadena. 

```console
optional arguments:
  -h, --help            show this help message and exit
  --f_user F_USER       Usuario de facebook
  --f_password F_PASSWORD
                        Password de facebook
  --f_busqueda F_BUSQUEDA
                        Busqueda en facebook
```
Ejemplos de uso:

```console
python main.py --f_user $VAR_USER --f_password $VAR_PASSWORD --f_busqueda $VAR_SEARCH
python main.py --f_user $VAR_USER --f_password $VAR_PASSWORD
```

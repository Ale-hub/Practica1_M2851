""" Script para web scraping del portal fotocasa.es
- robots.txt: https://www.fotocasa.es/robots.txt
- Tamaño site:fotocasa.es aproximadamente 1.590.000 resultados

¡¡IMPORTANTE!! Para el correcto funcionamiento del paquete Selenium se requiere la instalación del webdriver
del navegador y la ruta correcta al driver. Para configurar correctamente el script hay que modificar las
variables chromrdriver y osEnvironElement. También en la linea 40 se debe hacer una modificación para usar un
método distinto al webdriver.Chrome si fuera necesario.
"""

# Librerías
import time
from datetime import date
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pandas as pd

# Variables
chromrdriver = "./chromedriver"
osEnvironElement = "webdriver.chrome.driver"

urlBase = "https://www.fotocasa.es"
urlTipoAnuncio = {"Comprar": "/es/comprar/viviendas/las-palmas-provincia/gran-canaria/l",
                  "Alquilar": "/es/alquiler/viviendas/las-palmas-provincia/gran-canaria/l",
                  "Obra Nueva": "/es/promociones-obra-nueva/alquiler/viviendas/las-palmas-provincia/gran-canaria/l"
                  }

paginacion = 100
csvName = r"\csv\anuncios_" + date.today().strftime("%Y-%m-%d") + ".csv"
pathCSV = os.getcwd()
output_file = pathCSV + csvName


# Funciones


def webDriver_scrollDown(driverPath, osEnvironEle, url):
    os.environ[osEnvironEle] = driverPath

    opts = Options()
    opts.add_argument("--headless")

    driver = webdriver.Chrome(executable_path=driverPath, options=opts)
    driver.get(url)

    # Pausa de precaución para evitar bloqueo
    time.sleep(0.4)

    # Hacemos scroll en la web para generar el contenido
    try:
        bodyElement = driver.find_element_by_tag_name('body')
        Scrolls = 30

        for i in range(1, Scrolls):
            bodyElement.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.5)

    except Exception as err1:
        print("Error haciendo scroll down: {}".format(err1))

    # Guardamos el resultado en una variable después de hacer scroll
    page_source = driver.page_source

    # Eliminamos cookies y terminamos el driver
    driver.delete_all_cookies()
    driver.close()

    return page_source


def scrap_anuncios(maxPagination, driver, osEnvElement, urldomain, tiposAnuncios):
    listaLinks = []
    listaTitulos = []
    listaPrecio = []
    listaFeatures = []
    listaLocalizacion = []
    listaTipoInmueble = []
    listaTipoAnuncio = []

    # Bucle para scrapear los 3 tipos de anuncios de vivienda.
    for tipoAnuncio, urlTipo in tiposAnuncios.items():
        nextPage = urldomain + urlTipo
        pageNumber = 0

        while pageNumber < maxPagination:
            time.sleep(0.5)
            print("Comenzando scrap en {} página {}. {}".format(tipoAnuncio, pageNumber + 1, nextPage))

            # Lanzamos el webdriver para hacer scroll
            html_source = webDriver_scrollDown(driver, osEnvElement, nextPage)

            # Usamos BeatifulSoup para leer el HTML que hemos capturado con webDriver_scrollDown()
            soup = BeautifulSoup(html_source, features="html.parser")

            # Extraemos toda la información de interés de todas las tarjetas de anuncios.
            for cardLink in soup.find_all("a", class_="re-Card-link", href=True):
                listaLinks.append(cardLink.get('href'))
                listaTitulos.append(cardLink.get('title'))
                listaPrecio.append(cardLink.findChildren("span", class_="re-Card-price")[0].get_text())
                listaFeatures.append(
                    [child.get_text() for child in cardLink.find("div", class_="re-CardFeatures-wrapper")
                        .find_all("span")])

                if cardLink.find("h3", class_="re-Card-title").find("span") is None:
                    listaTipoInmueble.append(None)
                    listaLocalizacion.append(cardLink.find("h3", class_="re-Card-title").contents[0])
                else:
                    listaTipoInmueble.append(cardLink.find("h3", class_="re-Card-title").contents[0].get_text())
                    listaLocalizacion.append(cardLink.find("h3", class_="re-Card-title").contents[1])

                listaTipoAnuncio.append(tipoAnuncio)

            # Si no hay más páginas terminamos con el bucle while.
            if soup.find("span", class_="sui-AtomButton-rightIcon") is None:
                print("Paginación superior a la disponible en anuncios tipo {}. ".format(tipoAnuncio) +
                      "Paginación fijada en {} y han sido leidas {}".format(maxPagination, pageNumber + 1))
                break
            else:
                clase = "sui-LinkBasic sui-AtomButton sui-AtomButton--primary sui-AtomButton--outline " \
                        "sui-AtomButton--center sui-AtomButton--small sui-AtomButton--link sui-AtomButton--empty"
                nextPage = urldomain + soup.find("span",
                                               class_="sui-AtomButton-rightIcon").find_parent("a",
                                                                                              class_=clase).get("href")
            pageNumber += 1

    df = pd.DataFrame(
        {"href": listaLinks,
         "title": listaTitulos,
         "price": listaPrecio,
         "features": listaFeatures,
         "propertyType": listaTipoInmueble,
         "shortLocation": listaLocalizacion,
         "adType": listaTipoAnuncio
         }
    )

    df["date"] = pd.to_datetime('today').strftime("%Y/%m/%d")

    return df


# Creamos un dataframe con los resultados del scraping web
anunciosDF = scrap_anuncios(paginacion, chromrdriver, osEnvironElement, urlBase, urlTipoAnuncio)

# Lo exportamos como csv con la fecha de ejecución.
anunciosDF.to_csv(output_file, sep=";", index=False, header=True, encoding='utf-8')

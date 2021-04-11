'''
Script para web scraping del portal fotocasa.es
- robots.txt: https://www.fotocasa.es/robots.txt
- Tamaño site:fotocasa.es aproximadamente 1.590.000 resultados
'''

# Librerías
import time
import requests
from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# Inicializamos variables
urlBase = "https://www.fotocasa.es/es/"
headers = {
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,\
*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"Accept-Encoding": "gzip, deflate",
"Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
"Cache-Control": "no-cache",
"dnt": "1",
"Pragma": "no-cache",
"Upgrade-Insecure-Requests": "1",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
(KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
}
chromrdriver = "./chromedriver"
os.environ["webdriver.chrome.driver"] = chromrdriver

# Instanciamos el webdriver
opts = Options()
opts.add_argument("--headless")
driver = webdriver.Chrome(executable_path=chromrdriver, options=opts)
driver.get("https://medium.com/search?q=data%20science")
time.sleep(0.4)
# Hacemos scroll en la web para generar el contenido
try:
    bodyElement = driver.find_element_by_tag_name('body')
    Scrolls = 30
    for i in range(1, Scrolls):
        bodyElement.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.7)
except Exception as err1:
    print("Error haciendo scroll down: {}".format(err1))
# Guardamos el resultado en una variable después de hacer scroll
page_source = driver.page_source
# Eliminamos cookies y terminamos el driver
driver.delete_all_cookies()
driver.close()

# Usamos BeatifulSoup para leer el HTML que hemos capturado con Selenium
soup = BeautifulSoup(page_source, features="html.parser")
# Extraemos los enlaces de los enlaces de los anuncios y los almacenamos.
listaLinks = []
listaTitulos = []
listaPrecio = []
for link in soup.find_all("a", class_=".re-Card-link", href=True):
    listaLinks.append(link.get('href'))
    listaTitulos.append(link.get('title'))
    listaPrecio.append(link.findChildren("span", class_="re-Card-price")[0].get_text())
    print(link)
# Definimos t0 como el instante de tiempo de antes de lanzar la petición para medir el tiempo de respuesta.
t0 = time.time()
# Petición
try:
    page = requests.get(urlBase, timeout=15)
except requests.exceptions.RequestException as err:
    print("Error: {}. URL: {}".format(err, urlBase))

# Medimos el tiempo de respuesta
response_delay = time.time() - t0
# Pausamos la consecución de la instrucciones un tiempo prudente de 10 veces el tiempo de respuesta.
time.sleep(10 * response_delay)
# Código de estado de la respuesta
#print(page.status_code)
# Contenido de la respuesta
soup = BeautifulSoup(page.content)
print(soup.prettify())

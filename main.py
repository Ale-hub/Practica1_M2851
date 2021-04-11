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

<div class="u-paddingTop20 u-paddingBottom25 u-borderBottomLight js-block"><div class="postArticle postArticle--short js-postArticle js-trackPostPresentation" data-post-id="7ecc408b53c7" data-source="search_post---------0"><div class="u-clearfix u-marginBottom15 u-paddingTop5"><div class="postMetaInline u-floatLeft u-sm-maxWidthFullWidth"><div class="u-flexCenter"><div class="postMetaInline-avatar u-flex0"><a class="link u-baseColor--link avatar" href="https://towardsdatascience.com/@harrisonjansma" data-action="show-user-card" data-action-value="f78a75e220e5" data-action-type="hover" data-user-id="f78a75e220e5" data-collection-slug="towards-data-science" dir="auto"><img src="https://cdn-images-1.medium.com/fit/c/36/36/1*Kj7YffsuqBrS6H4QMfuB_Q.jpeg" class="avatar-image u-size36x36 u-xs-size32x32" alt="Go to the profile of Harrison Jansma"></a></div><div class="postMetaInline postMetaInline-authorLockup ui-captionStrong u-flex1 u-noWrapWithEllipsis"><a class="ds-link ds-link--styleSubtle link link--darken link--accent u-accentColor--textNormal u-accentColor--textDarken" href="https://towardsdatascience.com/@harrisonjansma?source=search_post---------0" data-action="show-user-card" data-action-source="search_post---------0" data-action-value="f78a75e220e5" data-action-type="hover" data-user-id="f78a75e220e5" data-collection-slug="towards-data-science" dir="auto">Harrison Jansma</a> in <a class="ds-link ds-link--styleSubtle link--darken link--accent u-accentColor--textNormal" href="https://towardsdatascience.com?source=search_post---------0" data-action="show-collection-card" data-action-source="search_post---------0" data-action-value="towards-data-science" data-action-type="hover" data-collection-slug="towards-data-science">Towards Data Science</a><div class="ui-caption u-fontSize12 u-baseColor--textNormal u-textColorNormal js-postMetaInlineSupplemental"><a class="link link--darken" href="https://towardsdatascience.com/how-to-learn-data-science-if-youre-broke-7ecc408b53c7?source=search_post---------0" data-action="open-post" data-action-value="https://towardsdatascience.com/how-to-learn-data-science-if-youre-broke-7ecc408b53c7?source=search_post---------0" data-action-source="preview-listing"><time datetime="2018-09-16T05:02:02.070Z">Sep 16, 2018</time></a><span class="middotDivider u-fontSize12"></span><span class="readingTime" title="9 min read"></span><span class="u-paddingLeft4"><span class="svgIcon svgIcon--star svgIcon--15px"><svg class="svgIcon-use" width="15" height="15"><path d="M7.438 2.324c.034-.099.09-.099.123 0l1.2 3.53a.29.29 0 00.26.19h3.884c.11 0 .127.049.038.111L9.8 8.327a.271.271 0 00-.099.291l1.2 3.53c.034.1-.011.131-.098.069l-3.142-2.18a.303.303 0 00-.32 0l-3.145 2.182c-.087.06-.132.03-.099-.068l1.2-3.53a.271.271 0 00-.098-.292L2.056 6.146c-.087-.06-.071-.112.038-.112h3.884a.29.29 0 00.26-.19l1.2-3.52z"></path></svg></span></span></div></div></div></div></div><div class="postArticle-content"><a href="https://towardsdatascience.com/how-to-learn-data-science-if-youre-broke-7ecc408b53c7?source=search_post---------0" data-action="open-post" data-action-source="search_post---------0" data-action-value="https://towardsdatascience.com/how-to-learn-data-science-if-youre-broke-7ecc408b53c7?source=search_post---------0" data-action-index="0" data-post-id="7ecc408b53c7"><section class="section section--body section--first section--last"><div class="section-divider"><hr class="section-divider"></div><div class="section-content"><div class="section-inner sectionLayout--insetColumn"><figure name="previewImage" id="previewImage" class="graf graf--figure graf--layoutCroppedHeightPreview graf--leading"><div class="aspectRatioPlaceholder is-locked"><div class="aspectRatioPlaceholder-fill" style="padding-bottom: 30%;"></div><div class="progressiveMedia js-progressiveMedia graf-image is-canvasLoaded is-imageLoaded" data-image-id="0*zV1Hxq8zOqi7oEQS" data-width="4608" data-height="2880" data-is-featured="true" data-scroll="native"><img src="https://cdn-images-1.medium.com/freeze/fit/t/30/9/0*zV1Hxq8zOqi7oEQS?q=20" crossorigin="anonymous" class="progressiveMedia-thumbnail js-progressiveMedia-thumbnail"><canvas class="progressiveMedia-canvas js-progressiveMedia-canvas" width="75" height="22"></canvas><img class="progressiveMedia-image js-progressiveMedia-image" data-src="https://cdn-images-1.medium.com/fit/t/800/240/0*zV1Hxq8zOqi7oEQS" src="https://cdn-images-1.medium.com/fit/t/800/240/0*zV1Hxq8zOqi7oEQS"><noscript class="js-progressiveMedia-inner"><img class="progressiveMedia-noscript js-progressiveMedia-inner" src="https://cdn-images-1.medium.com/fit/t/800/240/0*zV1Hxq8zOqi7oEQS"></noscript></div></div></figure><h3 name="3f4e" id="3f4e" class="graf graf--h3 graf-after--figure graf--title">How To Learn Data Science If You’re&nbsp;Broke</h3><p name="f496" id="f496" class="graf graf--p graf-after--h3 graf--trailing">Over the last year, I taught myself data science. I learned from hundreds of online…</p></div></div></section></a></div><div class="postArticle-readMore"><a class="button button--smaller button--chromeless u-baseColor--buttonNormal" href="https://towardsdatascience.com/how-to-learn-data-science-if-youre-broke-7ecc408b53c7?source=search_post---------0" data-action="open-post" data-action-source="search_post---------0" data-action-value="https://towardsdatascience.com/how-to-learn-data-science-if-youre-broke-7ecc408b53c7?source=search_post---------0" data-post-id="7ecc408b53c7">Read more…</a></div><div class="u-clearfix u-paddingTop10"><div class="u-floatLeft"><div class="multirecommend js-actionMultirecommend u-flexCenter" data-post-id="7ecc408b53c7" data-is-flush-left="true" data-source="listing-----7ecc408b53c7---------------------clap_preview"><div class="u-relative u-foreground"><button class="button button--primary button--chromeless u-accentColor--buttonNormal button--withIcon button--withSvgIcon clapButton js-actionMultirecommendButton clapButton--darker" data-action="sign-up-prompt" data-sign-in-action="multivote" data-requires-token="true" data-redirect="https://medium.com/_/vote/p/7ecc408b53c7" data-action-source="listing-----7ecc408b53c7---------------------clap_preview" aria-label="Clap"><span class="button-defaultState"><span class="svgIcon svgIcon--clap svgIcon--25px is-flushLeft"><svg class="svgIcon-use" width="25" height="25"><g fill-rule="evenodd"><path d="M11.739 0l.761 2.966L13.261 0z"></path><path d="M14.815 3.776l1.84-2.551-1.43-.471z"></path><path d="M8.378 1.224l1.84 2.551L9.81.753z"></path><path d="M20.382 21.622c-1.04 1.04-2.115 1.507-3.166 1.608.168-.14.332-.29.492-.45 2.885-2.886 3.456-5.982 1.69-9.211l-1.101-1.937-.955-2.02c-.315-.676-.235-1.185.245-1.556a.836.836 0 01.66-.16c.342.056.66.28.879.605l2.856 5.023c1.179 1.962 1.379 5.119-1.6 8.098m-13.29-.528l-5.02-5.02a1 1 0 01.707-1.701c.255 0 .512.098.707.292l2.607 2.607a.442.442 0 00.624-.624L4.11 14.04l-1.75-1.75a.998.998 0 111.41-1.413l4.154 4.156a.44.44 0 00.624 0 .44.44 0 000-.624l-4.152-4.153-1.172-1.171a.998.998 0 010-1.41 1.018 1.018 0 011.41 0l1.172 1.17 4.153 4.152a.437.437 0 00.624 0 .442.442 0 000-.624L6.43 8.222a.988.988 0 01-.291-.705.99.99 0 01.29-.706 1 1 0 011.412 0l6.992 6.993a.443.443 0 00.71-.501l-1.35-2.856c-.315-.676-.235-1.185.246-1.557a.85.85 0 01.66-.16c.342.056.659.28.879.606L18.628 14c1.573 2.876 1.067 5.545-1.544 8.156-1.396 1.397-3.144 1.966-5.063 1.652-1.713-.286-3.463-1.248-4.928-2.714zM10.99 5.976l2.562 2.562c-.497.607-.563 1.414-.155 2.284l.265.562-4.257-4.257a.98.98 0 01-.117-.445c0-.267.104-.517.292-.706a1.023 1.023 0 011.41 0zm8.887 2.06c-.375-.557-.902-.916-1.486-1.011a1.738 1.738 0 00-1.342.332c-.376.29-.61.656-.712 1.065a2.1 2.1 0 00-1.095-.562 1.776 1.776 0 00-.992.128l-2.636-2.636a1.883 1.883 0 00-2.658 0 1.862 1.862 0 00-.478.847 1.886 1.886 0 00-2.671-.012 1.867 1.867 0 00-.503.909c-.754-.754-1.992-.754-2.703-.044a1.881 1.881 0 000 2.658c-.288.12-.605.288-.864.547a1.884 1.884 0 000 2.659l.624.622a1.879 1.879 0 00-.91 3.16l5.019 5.02c1.595 1.594 3.515 2.645 5.408 2.959a7.16 7.16 0 001.173.098c1.026 0 1.997-.24 2.892-.7.279.04.555.065.828.065 1.53 0 2.969-.628 4.236-1.894 3.338-3.338 3.083-6.928 1.738-9.166l-2.868-5.043z"></path></g></svg></span></span><span class="button-activeState"><span class="svgIcon svgIcon--clapFilled svgIcon--25px is-flushLeft"><svg class="svgIcon-use" width="25" height="25"><g fill-rule="evenodd"><path d="M11.738 0l.762 2.966L13.262 0z"></path><path d="M16.634 1.224l-1.432-.47-.408 3.022z"></path><path d="M9.79.754l-1.431.47 1.84 2.552z"></path><path d="M22.472 13.307l-3.023-5.32c-.287-.426-.689-.705-1.123-.776a1.16 1.16 0 00-.911.221c-.297.231-.474.515-.535.84.017.022.036.04.053.063l2.843 5.001c1.95 3.564 1.328 6.973-1.843 10.144a8.46 8.46 0 01-.549.501c1.205-.156 2.328-.737 3.351-1.76 3.268-3.268 3.041-6.749 1.737-8.914"></path><path d="M12.58 9.887c-.156-.83.096-1.569.692-2.142L10.78 5.252c-.5-.504-1.378-.504-1.879 0-.178.18-.273.4-.329.63l4.008 4.005z"></path><path d="M15.812 9.04c-.218-.323-.539-.55-.88-.606a.814.814 0 00-.644.153c-.176.137-.713.553-.24 1.566l1.43 3.025a.539.539 0 11-.868.612L7.2 6.378a.986.986 0 10-1.395 1.395l4.401 4.403a.538.538 0 11-.762.762L5.046 8.54 3.802 7.295a.99.99 0 00-1.396 0 .981.981 0 000 1.394L3.647 9.93l4.402 4.403a.537.537 0 010 .761.535.535 0 01-.762 0L2.89 10.696a.992.992 0 00-1.399-.003.983.983 0 000 1.395l1.855 1.854 2.763 2.765a.538.538 0 01-.76.761l-2.765-2.764a.982.982 0 00-1.395 0 .989.989 0 000 1.395l5.32 5.32c3.371 3.372 6.64 4.977 10.49 1.126C19.74 19.8 20.271 17 18.62 13.982L15.812 9.04z"></path></g></svg></span></span></button></div><span class="u-relative u-background js-actionMultirecommendCount u-marginLeft5"><button class="button button--chromeless u-baseColor--buttonNormal js-multirecommendCountButton u-disablePointerEvents" data-action="show-recommends" data-action-value="7ecc408b53c7">22K</button></span></div></div><div class="buttonSet u-floatRight"><a class="button button--chromeless u-baseColor--buttonNormal" href="https://towardsdatascience.com/how-to-learn-data-science-if-youre-broke-7ecc408b53c7?source=search_post---------0#--responses" data-action-source="search_post---------0">72 responses</a><button class="button button--dark button--chromeless is-touchIconFadeInPulse u-baseColor--buttonDark button--withIcon button--withSvgIcon button--bookmark js-bookmarkButton" data-action="add-to-bookmarks" data-action-value="7ecc408b53c7"><span class="js-remove-from-bookmarks u-hide"><span class="svgIcon svgIcon--bookmarkFilled svgIcon--25px is-flushRight"><svg class="svgIcon-use" width="25" height="25"><path d="M19 6c0-1.1-.9-2-2-2H8c-1.1 0-2 .9-2 2v14.66h.012c.01.103.045.204.12.285a.5.5 0 00.706.03L12.5 16.85l5.662 4.126c.205.183.52.17.708-.03a.5.5 0 00.118-.285H19V6z"></path></svg></span></span><span class="js-add-to-bookmarks"><span class="svgIcon svgIcon--bookmark svgIcon--25px is-flushRight"><svg class="svgIcon-use" width="25" height="25"><path d="M19 6c0-1.1-.9-2-2-2H8c-1.1 0-2 .9-2 2v14.66h.012c.01.103.045.204.12.285a.5.5 0 00.706.03L12.5 16.85l5.662 4.126a.508.508 0 00.708-.03.5.5 0 00.118-.285H19V6zm-6.838 9.97L7 19.636V6c0-.55.45-1 1-1h9c.55 0 1 .45 1 1v13.637l-5.162-3.668a.49.49 0 00-.676 0z" fill-rule="evenodd"></path></svg></span></span></button></div></div></div></div>

# No pude tomar el código html de l pagina. Por este  error: ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1123)
# por eso deje como comentario esta parte y llamé de un documento el código
#page = requests.get('https://scienti.minciencias.gov.co/ciencia-war/')
#tree = html.fromstring(page.content)
#tree1 = html.fromstring(page.status_code)
#print(tree)
#import requests
#import certifi
#certifi.where()

from bs4 import BeautifulSoup
from lxml import html

with open('home_scienti.html', 'r') as html_file:
    content = html_file.read()
    soup = BeautifulSoup(content, 'lxml')
    #print(soup.prettify())
    tipo_grupos_html = soup.find_all('a')
    for tipo_grupos in tipo_grupos_html:
        print(tipo_grupos.text)




from bs4 import BeautifulSoup
import requests
from lxml import html
import csv

# No pude tomar el código html de l pagina. Por este  error: ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1123)
# por eso deje como comentario esta parte y llamé de un documento el código
#html_text = requests.get('https://scienti.minciencias.gov.co/ciencia-war/busquedaConteoGrupoXProgramaNacional.do?by=primario&codPrograma=2').text
#print(html_text)

with open('home2_scienti.html', 'r') as html_file:
    content = html_file.read()
    soup = BeautifulSoup(content, 'lxml')
    info_grupos = soup.find_all('tbody', class_='tbody' )
    for info_grupo in info_grupos:
        cods = info_grupo.find_all('td')
        #for cod in cods:
         #   cod = cod.find_all('td')
          #  print(cod)
    print(cods)


# Encontre este ejemplo en internet pero no funcionó
#class tablescraper:
 #   def fetch(self, url):
  #      return requests.get(url)

    #def parse(self, html):
      #  content = BeautifulSoup(html, 'lxml')
       # table = content.find('table')
        #rows = table.findAll('tr')
        #print(rows)

#    def to_csv(self):
 #       pass

 #   def run(self):
  #      response = self.fetch('https://scienti.minciencias.gov.co/ciencia-war/busquedaConteoGrupoXProgramaNacional.do?by=primario&codPrograma=2')
   #     self.parse(response.text)

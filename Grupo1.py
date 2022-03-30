from bs4 import BeautifulSoup
import requests
from lxml import html

#html_text = requests.get('https://scienti.minciencias.gov.co/ciencia-war/busquedaConteoGrupoXProgramaNacional.do?by=primario&codPrograma=2').text
#print(html_text)

with open('home2_scienti.html', 'r') as html_file:
    content = html_file.read()
    soup = BeautifulSoup(content, 'lxml')
    #print(soup.prettify())
    grupos1_html_tags = soup.find_all('tbody')
    for grupos1 in grupos1_html_tags:
       print(grupos1)
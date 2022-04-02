import requests
import csv
from bs4 import BeautifulSoup

url_base = 'https://scienti.minciencias.gov.co/ciencia-war/'
archivo_csv = 'salida.csv'


def obtener_pagina(sesion, url):
    return BeautifulSoup(sesion.get(url, verify=False).content, "html.parser")


def obtener_complemento_url(pagina):
    categoria = 'Categor%EDa+A'
    numero_grupos = '100'
    return ("?by=union&codPrograma=2&codRh=&codAreaConocimiento="
                  "&maxRows={}&grupos_tr_=true"
                  "&grupos_p_={}"
                  "&grupos_mr_={}"
                  "&grupos_f_tpoEstado={}").format(numero_grupos, pagina, numero_grupos, categoria)


def detener_ciclo(tr, tds):
    detener = False
    # Detectar fin de ciclo (control GIF - nextPage.gif o nextPageDisabled.gif )
    if tr.attrs.get('class') is not None:
        if tr.attrs['class'][0] == 'toolbar':
            if len(tds) > 3:
                if tds[3].contents[0].attrs.get('src') is not None:
                    gif = tds[3].contents[0].attrs['src']
                    if "nextPageDisabled.gif" in gif:
                            detener = True

    return detener


def obtener_renglon_csv(tds, pn, pns):
    r_csv = ''
    if len(tds) > 7:
        id = tds[0].text
        codigo_grupo = tds[1].text
        nombre_grupo = '"' + tds[2].text + '"'
        lider = tds[3].text
        avalado = tds[5].text
        estado = tds[6].text
        calificado_en = tds[7].text
        r = [id, codigo_grupo, nombre_grupo, lider, avalado, estado, calificado_en, pn, pns]
        r_csv = ",".join(r) + "\n\r"
    return r_csv


with requests.Session() as session:
    # recuperar pagina de inicio y obtener url del "GRUPO"
    pagina_inicio = obtener_pagina(session, url_base)
    enlaces = pagina_inicio.find_all("a", text="Grupos por Programa Nacional de Ciencia y Tecnología")
    enlace = enlaces[0].attrs['href']

    # recuperar pagina de programas y obtener url del "PROGRAMA - (AMBOS)"
    pagina_programas = obtener_pagina(session, url_base + enlace)
    enlaces_ambos = pagina_programas.find_all("a", text="./busquedaConteoGrupoXProgramaNacional.do?by=union&amp;codPrograma=2")
    enlace_ambos = enlaces_ambos.source.text
    tabla_url = enlace_ambos.split('?')

    # ciclar por cada pagina de tabla hasta DETENER==True o hasta 10 solicitudes de pagina
    detener = False
    detener2 = False
    pagina = 1
    while detener2 == False and pagina < 10:
        tabla_enlace = url_base + tabla_url[0] + obtener_complemento_url(pagina)
        pagina += 1
        pagina_tabla_n = obtener_pagina(session, tabla_enlace)

        # Busca la primera tabla con id = grupos
        tablas = pagina_tabla_n.find_all(id="grupos")
        tabla_trs = tablas[0].select('tr')

        r_csv = ""
        for tr in tabla_trs:
            tds = tr.select('td')
            detener = detener_ciclo(tr, tds)
            if detener == True:
                detener2 = True

            if tr.attrs.get('class') is not None:
                clase = tr.attrs['class'][0]
                if tr.attrs['class'][0] == 'odd' or tr.attrs['class'][0] == 'even':
                    # recuperar HREF de pagina de perfiles (PRIMARIO O SECUNDARIO)
                    if len(tds) > 7:
                        if tds[4].contents[0].attrs.get('href') is not None:
                            href_perfil = tds[4].contents[0].attrs['href']
                            # pagina_perfil = obtener_pagina(session, href_perfil)
                            # p_tds = pagina_perfil.find_all('td', {"class": "sinBorde"})
                            prog_nacional =''
                            prog_nacional_secundario = ''
                            cnt = 0
                            # for p_td in p_tds:
                                #  if "Programa Nacional:" in p_td.text:
                                    # prog_nacional = p_tds[cnt + 1].text.strip()
                                    # prog_nacional_secundario = p_tds[cnt + 3].text.strip()
                                # cnt += 1
                    # obtener el renglon csv con tabla mas programas
                    r_csv += obtener_renglon_csv(tds, prog_nacional, prog_nacional_secundario)

        # si se encontro renglon, agregarlo al archivo csv
        if r_csv != '':
            with open('out.csv', 'a') as archivo:
                archivo.write(r_csv)

print("fin de proceso")





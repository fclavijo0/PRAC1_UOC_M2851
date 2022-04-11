# Título: Dataset de los grupos de investigación colombianos con categoría A y A1 y que hacen parte de los Programas Nacionales de Ciencia,
# Tecnología e Innovación en Salud e Ingeniería. 

# Descripción: Este repositorio se crea como parte de una práctica de la asignatura M2.851 - Tipología y ciclo de vida de los datos aula 1, de la UOC,
# en el Máster de Ciencia de Datos. En la cual se elaborará un caso práctico orientado a aprender a identificar los datos relevantes para un proyecto
# analítico y usar herramientas de extracción de datos.

# Autores: FEDERICO CLAVIJO LÓPEZ (fclavijo0) y ALEJANDRO MEDINA UICAB (amedinau)

import requests
import csv
import sys
import time
import datetime
from bs4 import BeautifulSoup


inicia = datetime.datetime.now().time().strftime('%H:%M:%S')

# Ignora los warnings conocidos.
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")


url_base = 'https://scienti.minciencias.gov.co/ciencia-war/'
archivo_csv = 'salida.csv'
MAXIMO_PAGINAS = 10  # máximo de consultas y evitar un ciclo infinito


def obtener_pagina(sesion, url):
    return BeautifulSoup(sesion.get(url, verify=False).content, "html.parser")


def obtener_complemento_url(pagina, programa, numero_grupos):
    categoria = 'Categor%EDa+A'
    return ("?by=union&codPrograma={}&codRh=&codAreaConocimiento="
                  "&maxRows={}&grupos_tr_=true"
                  "&grupos_p_={}"
                  "&grupos_mr_={}"
                  "&grupos_f_tpoEstado={}").format(programa, numero_grupos, pagina, numero_grupos, categoria)


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


def obtener_renglon_csv(tds, pn, pns, prog):
    r_csv = ''
    if len(tds) > 7:
        id = tds[0].text
        codigo_grupo = tds[1].text
        nombre_grupo = '"' + tds[2].text + '"'
        lider = tds[3].text
        avalado = tds[5].text
        estado = tds[6].text
        calificado_en = tds[7].text
        r = [id, codigo_grupo, nombre_grupo, lider, avalado, estado, calificado_en, pn, pns, prog]
        r_csv = ",".join(r) + '\n'
    return r_csv


with requests.Session() as session:
    # Verificar que existe el enlace en la página principal.
    pagina_inicio = obtener_pagina(session, url_base)
    enlaces = pagina_inicio.find_all("a", text="Grupos por Programa Nacional de Ciencia y Tecnología")
    enlace = enlaces[0].attrs['href']
    if enlace == '':
        print("Enlace no existe enlace: Grupos por Programa Nacional de Ciencia y Tecnología")
        exit()

    # Verificar que existen los enlaces en la segunda página.
    pagina_programas = obtener_pagina(session, url_base + enlace)
    enlaces_salud = pagina_programas.find_all("a", text="./busquedaConteoGrupoXProgramaNacional.do?by=union&amp;codPrograma=2")
    enlaces_ingenieria = pagina_programas.find_all("a", text="./busquedaConteoGrupoXProgramaNacional.do?by=union&amp;codPrograma=15")
    enlace_salud = enlaces_salud.source.text
    enlace_ingenieria = enlaces_ingenieria.source.text
    programas = {}
    if enlace_salud == '':
        print("No existe enlace Ciencia, Tecnologá e Innovación en Salud.")
    else:
        programas['2'] = "Salud."
    if enlace_ingenieria == '':
        print("No existe enlace Ciencia, Tecnología e Innovación en Ingeniería")
    else:
        programas['15'] = "Ingeniería"
    if len(programas) == 0:
        print("No hay enlaces para los programas de interés.")
        exit()
    tabla_url = enlace_salud.split('?')

    # crear archivo de salida y encabezados
    hd_csv_r = ['ID', 'Codigo de grupo', 'Nombre de grupo', 'Lider', 'Avalado', 'Estado', 'Calificado', 'Programa nacional', 'Programa nacional secundario', 'Programa tipo']
    hd_csv = ",".join(hd_csv_r) + "\n\r"
    with open(archivo_csv, 'w+', encoding='utf-8') as archivo:
        archivo.write(hd_csv)
        print("Se escribe :" + hd_csv)


    # Para cada programa, recuperar datos de grupos y perfiles (tercera y cuarta página)
    for programa_numero, programa_texto in programas.items():
        existe_gif = False  # al encontrar: nextPageDisabled.gif se llega al final de los registros
        detener = False
        pagina = 1
        while detener == False and pagina < MAXIMO_PAGINAS:
            numero_grupos = 100  # cuantos grupos muestra la consulta: 15, 50 o 100
            tabla_enlace = url_base + tabla_url[0] + obtener_complemento_url(pagina, programa_numero, numero_grupos)
            pagina += 1

            # Consulta la tercera página con la tabla de resultados
            pagina_tabla_n = obtener_pagina(session, tabla_enlace)
            print("Se obtiene página: " + tabla_enlace)
            tablas = pagina_tabla_n.find_all(id="grupos")
            tabla_trs = tablas[0].select('tr')
            r_csv = ""

            # Recorrer todos los renglones TR
            for tr in tabla_trs:
                tds = tr.select('td')
                existe_gif = detener_ciclo(tr, tds)  # Verificar si es el fin de los registros
                if existe_gif == True:
                    detener = True

                if tr.attrs.get('class') is not None:
                    clase = tr.attrs['class'][0]

                    # los renglones que tienen datos de interés tiene la clase ODD o EVEN
                    if tr.attrs['class'][0] == 'odd' or tr.attrs['class'][0] == 'even':
                        if len(tds) > 7:

                            # La columna TD 4 tiene el URL a la cuarta página
                            if tds[4].contents[0].attrs.get('href') is not None:
                                href_perfil = tds[4].contents[0].attrs['href']
                                prog_nacional = ''
                                prog_nacional_secundario = ''

                                if href_perfil != '':
                                    pagina_perfil = obtener_pagina(session, href_perfil)
                                    print("Se obtiene página: " + href_perfil)
                                    p_tds = pagina_perfil.find_all('td', {"class": "sinBorde"})
                                    cnt = 0

                                    # Buscar dentro del conjunto de renglones TDS la leyenda del programa
                                    for p_td in p_tds:
                                        if "Programa Nacional:" in p_td.text:
                                            prog_nacional = '"' + p_tds[cnt + 1].text.strip() + '"'
                                            prog_nacional_secundario = '"' + p_tds[cnt + 3].text.strip() + '"'
                                        cnt += 1
                        r_csv += obtener_renglon_csv(tds, prog_nacional, prog_nacional_secundario, programa_texto)
            if r_csv != '':
                with open(archivo_csv, 'a',  encoding='utf-8') as archivo:
                    archivo.write(r_csv)

termina = datetime.datetime.now().time().strftime('%H:%M:%S')
tiempo_total = (datetime.datetime.strptime(termina, '%H:%M:%S') - datetime.datetime.strptime(inicia, '%H:%M:%S'))
print("Fin de proceso. Tiempo total: ")
print(tiempo_total)





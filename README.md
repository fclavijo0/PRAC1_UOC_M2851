**PRACTICA 1 - Web scraping**

***Título: Dataset de los grupos de investigación colombianos con categoría A y A1 y que hacen parte de los Programas Nacionales de Ciencia, Tecnología e Innovación en Salud e Ingeniería.***

Este repositorio se crea como parte de una práctica de la asignatura M2.851 - Tipología y ciclo de vida de los datos aula 1, de la UOC, en el Máster de Ciencia de Datos. En la cual se elaborará un caso práctico orientado a aprender a identificar los datos relevantes para un proyecto analítico y usar herramientas de extracción de datos.

**CONTEXTO**

En Colombia, el Ministerio de Ciencia Tecnología e Innovación (Minciencias) regula, gestiona y financia la mayor parte de las actividades de innovación, investigación y desarrollo de tecnología, a través de diferentes convocatorias públicas y programas gubernamentales. En el marco de esta gestión Minciencias ha generado varias bases de datos para gestionar y divulgar de forma estructurada, la información concerniente a entidades que investigan, grupos de investigación, investigadores y convocatorias vigentes, a través de plataformas en línea de acceso público.

Una de estas plataformas fue escogida para el desarrollo de esta práctica (https://scienti.minciencias.gov.co/ciencia-war/) en ésta se puede acceder a las bases de datos que recogen toda la información sobre currículos de investigadores (CvLAC) y hojas de vida de grupos de investigación (GrupLAC) colombianos.

Si bien en la plataforma se puede consultar la información a través varios criterios, hay búsquedas que no se pueden realizar de forma sencilla e implica un proceso tedioso de filtrado manual. A partir de estas dificultades se decidió centrar esta práctica en: recaudar la información concerniente a los grupos de investigación que tengan categoía A y A1 y que hagan parte de los Programas Nacionales de Ciencia, Tecnología e Innovación en Salud y en Ingeniería, sin importar si estas son la temática principal o secundaria del grupo. Información consultada en esta pagina web: https://scienti.minciencias.gov.co/ciencia-war/busquedaConteoGrupoXProgramaNacional.do?by=primario&codPrograma=2

**GRUPO DE LA PRÁCTICA**
- FEDERICO CLAVIJO LÓPEZ (fclavijo0)
- ALEJANDRO MEDINA UICAB (amedinau)

**ARCHIVOS QUE HACEN PARTE DE LA ENTREGA**
- Codigo_practica.py - Corresponde al documento que contiene el código que realiza el web scraping a la página seleccionada.
- Salida.csv - Corresponde al documento de salida del proceso de web scraping que contiene los datos recabados de la página seleccionada.
- Desarrollo.ipynb - Corresponde al documento en formato ipynb y PDF que contiene las respuestas a las preguntas planteadas en la práctica 

Link al video: https://drive.google.com/drive/folders/1qtMCDjFYd46A-r2z0ZXQlq6_HxfYWuVf?usp=sharing
El dataset en Zenodo y el código DOI es: 10.5281/zenodo.6441181 Link: https://doi.org/10.5281/zenodo.6441181

**RECURSOS UTILIZADOS EN EL DESARROLLO DE LA PRÁCTICA**
- Subirats, L., Calvo, M. (2018). Web Scraping. Editorial UOC.
- Masip, D. (2019) El lenguaje Python. Editorial UOC.
- Lawson, R. (2015). Web Scraping with Python. Packt Publishing Ltd. Chapter 2. Scraping the Data.
- Simon Munzert, Christian Rubba, Peter Meißner, Dominic Nyhuis. (2015). Automated Data Collection with R: A Practical Guide to Web Scraping and Text Mining. John Wiley & Sons.

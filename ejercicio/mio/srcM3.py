'''
Created on 1 oct 2024

@author: alvaro
'''
# encoding:utf-8

from bs4 import BeautifulSoup
import urllib.request
from tkinter import *
from tkinter import messagebox
import sqlite3
import lxml
from datetime import datetime
# lineas para evitar error SSL
import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context


# ----- VENTANA PRINCIPAL -----------------------------------------------------------------------------------------
def ventana_principal():
    raiz = Tk()
    menu = Menu(raiz)
    
    # DATOS
    datosmenu = Menu(menu, tearoff=0)
    datosmenu.add_command(label="Cargar", command=cargar)
    datosmenu.add_separator()
    datosmenu.add_command(label="Salir", command=raiz.quit)
    menu.add_cascade(label="Datos", menu=datosmenu)
    
    # LISTAR
    listarmenu = Menu(menu, tearoff=0)
    listarmenu.add_command(label="Juegos", command=raiz.quit)
    listarmenu.add_command(label="Mejores juegos", command=raiz.quit)
    menu.add_cascade(label="Listar", menu=listarmenu)
    
    # BUSCAR
    buscarmenu = Menu(menu, tearoff=0)
    buscarmenu.add_command(label="Juegos por temática", command=raiz.quit)
    buscarmenu.add_command(label="Juegos por complejidad", command=raiz.quit)
    menu.add_cascade(label="Buscar", menu=buscarmenu)
    
    raiz.config(menu=menu)
    raiz.mainloop()
        

# ----- Funciones para la parte de DATOS ----------------------------------------------------------------------------
# Funciones de la parte de cargar
def cargar():
    respuesta = messagebox.askyesno(title="Confirmar", message="Está usted seguro que quiere recargar los datos?")
    if respuesta:
        almacenar_bd()


def almacenar_bd():
    conn = sqlite3.connect("juegos.db")
    conn.text_factory = str
    conn.execute("DROP TABLE IF EXISTS JUEGOS")
    conn.execute('''CREATE TABLE JUEGOS
        (TITULO            TEXT NOT NULL,
        PORCENTAJE         REAL,
        PRECIO             REAL,
        TEMATICA           TEXT,
        COMPLEJIDAD        TEXT);''')
    
    lista_link_juegos = extraer_url_elementos()
    for link_juego in lista_link_juegos:
        f = urllib.request.urlopen(link_juego)
        s = BeautifulSoup(f, "lxml")
        titulo = s.find("span", attrs={"data-ui-id":"page-title-wrapper"}).string.strip()
        porcentaje = s.find("div", class_="rating-result")
        if porcentaje:
            porcentaje = porcentaje["title"].replace("%", "")
        precio = s.find("meta", itemprop="price")["content"]
        tematica = s.find("div", attrs={"data-th":"Temática"})
        if tematica:
            tematica = tematica.string.strip()
        complejidad = s.find("div", attrs={"data-th":"Complejidad"})
        if complejidad:
            complejidad = complejidad.string.strip()
        print(tematica)
        print(complejidad)
    

def extraer_url_elementos():
    lista_link_juegos = []
    for num_paginas in range(1, 3):
        url = f'https://zacatrus.es/juegos-de-mesa.html?p={num_paginas}'
        f = urllib.request.urlopen(url)
        s = BeautifulSoup(f, "lxml")
        lista_una_pagina = s.find_all("li", class_="item product product-item")
        for juego in lista_una_pagina:
            url_juego = juego.a['href']
            lista_link_juegos.append(url_juego)
    return lista_link_juegos

# ----- Funciones para la parte de LISTAR ----------------------------------------------------------------------------
# Funciones de la parte de juegos

# Funciones de la parte mejores juegos

# ----- Funciones para la parte de BUSCAR ----------------------------------------------------------------------------
# Función de la parte de buscar juegos por temática

# Función de la parte de buscar juegos por complejidad


# ----- TEST --------------------------------------------------------------------------------------------
if __name__ == "__main__":
    ventana_principal()
    print("Programa finalizado!")
    

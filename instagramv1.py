# -*- coding: utf-8 -*-
""" Created on Sat Dec 28 22:04:43 2019 @author: 
sebas """
#pip install selenium
from selenium import webdriver
#Instalar chromedriver para que abre el Chromium 
#para visitar la pagina web pip install 
#beautifulsoap
from bs4 import BeautifulSoup as bs import time 
import re from urllib.request import urlopen import 
ssl from math import ceil def 
obtenerLinksPublicacionesInstagram(username):
    numero_Links_A_encontrar = 12
    max_cnt = ceil(numero_Links_A_encontrar/12)
    print(max_cnt)
    browser = 
webdriver.Chrome("C:\\chromedriver_win32\\chromedriver.exe")
    browser.get('https://www.instagram.com/'+username+'/?hl=en')
    Pagelength = 
browser.execute_script("window.scrollTo(0, 
document.body.scrollHeight);")
    links=[]
    
    cnt = 0
    while cnt < max_cnt:
        if cnt == 0:
            texto_variable="window.scrollTo(0, 
document.body.scrollHeight/1.5);"
        else:
            texto_variable 
="window.scrollTo(document.body.scrollHeight/" + 
str(1.5*cnt) + ", document.body.scrollHeight/" + 
str(1.5*(cnt+1)) + ");"
            
#        print(texto_variable)
        Pagelength = 
browser.execute_script(texto_variable)
        cnt += 1
        source = browser.page_source
        data=bs(source, 'html.parser')
        #print(data)
        body = data.find('body')
        #print(body)
        script = body.find('div')
        #print(type(script))
        
        time.sleep(5)
        
        for link in script.findAll('a'):
            #print(link)
            if re.match("/p", link.get('href')):
                #print('ENCONTRO UN HREF')
                links.append('https://www.instagram.com'+link.get('href'))
        
#    print(links)
    browser.quit()
    return links def 
enviar_Notif_si_ecuentra_info(url, 
mensaje_a_buscar):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    html = urlopen(url, context=ctx).read()
        
#        handler= open("datos.html","wb") 
#        handler.write(html) handler.close()
        
    soup = bs(html, 'html.parser')
    datos = soup.find_all('title')
#        print(datos)
    
    datos = str(datos[0])
    for palabra in datos.split():
        if palabra == mensaje_a_buscar:
            print("ECONTRADO: --- ", 
mensaje_a_buscar, " ---")
            print(datos) def 
busqueda_info_Publicaciones_Inst(username,mensaje_a_buscar):
    urls = 
obtenerLinksPublicacionesInstagram(username)
    for url in urls:
        enviar_Notif_si_ecuentra_info(url, 
mensaje_a_buscar)
        
username='supercines'
#mensaje_a_buscar='#DíadeLocura'
mensaje_a_buscar='vermouth' 
busqueda_info_Publicaciones_Inst(username,mensaje_a_buscar) 
def borrarLinksRepetidos(urls):
    urls=sorted(urls)
#    print(urls)
    new_urls = []
    i=0
    while i < len(urls):
#        print(i) print(urls[i])
        if urls.count(urls[i]) > 1:
            cnt = urls.count(urls[i])
#            print(cnt)
            new_urls.append(urls[i])
            i += cnt
        else:
            new_urls.append(urls[i])
            i += 1
        
    return new_urls

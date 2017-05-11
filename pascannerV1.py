#!/usr/bin/python
from bs4 import BeautifulSoup
import requests
import re
import sys, getopt
from argparse import ArgumentParser



def attack():
    print "[*] Comenzando ataque.. "

def help():
    commands = {
                '-s': 'Indica el tipo de sector (Informatica, Telecomunicaciones..) PROXIMAMENTE',
                '-l': 'Indica el lugar (A Coruna, Barcelona..) PROXIMAMENTE',
                '-p': 'Indica el numero de paginas [1, 2.. (Por defecto 1]',
    }
    for clave, valor in commands.iteritems():
        print (clave, valor)

def search():

    url = 'https://www.paginasamarillas.es/search/informatica/all-ma/all-pr/all-is/all-ci/all-ba/all-pu/all-nc/'+pagina+'?cp='+lugar+'&what=informatica&where='+lugar+'&ub=false&qc=true'
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    if 'https://www.paginasamarillas.es/search/informatica/all-ma/all-pr/all-is/all-ci/all-ba/all-pu/all-nc/'+'1999'+'?cp='+lugar+'&what=informatica&where='+lugar+'&ub=false&qc=true' in url:
        links = soup.find_all('a', attrs={'itemprop': re.compile("^url")})
        for link in links:
            try:
                linkk = link.get('href')
                req2 = requests.get(linkk, allow_redirects=False)
                html2 = req2.text
                soup = BeautifulSoup(html2, 'html.parser')
                links = soup.find_all('meta')
                linksW = soup.find_all('link')
                strLink = str(links)
                strLinkW = str(linksW)
                if "WordPress" in strLink or "wp-content" in strLinksW:
                    print link.get('href') + ' - [WORDPRESS]'
                elif "Joomla" in strLink:
                    print link.get('href') + ' - [JOOMLA]'
                elif "Drupal" in strLink:
                    print link.get('href') + ' - [DRUPAL]'
                elif "PrestaShop" in strLink:
                    print link.get('href') + ' - [PRESTASHOP]'
                else:
                    print link.get('href') + ' - [NOCMS]'
            except requests.exceptions.ConnectionError as error:
                 continue

    else:
        links2 = soup.find_all('a')
        for link2 in links2:
            try:
                strLink = str(link2)
                if "businessId" in strLink:
                    webs = link2.get('href')
                    req = requests.get(webs)
                    html = req.text
                    soup = BeautifulSoup(html, 'html.parser')
                    links = soup.find_all('a', attrs={'itemprop': re.compile("^url")})
                    for link in links:
                        linkk = link.get('href')
                        req2 = requests.get(linkk)
                        html2 = req2.text
                        soup2 = BeautifulSoup(html2, 'html.parser')
                        links = soup2.find_all('meta')
                        strLink = str(links)
                        # Almacena el atributo content donde sale la version de WordPress
                        WPVersions = soup2.find_all('meta', attrs={"content":re.compile("^WordPress.?.")})
                        JOOVersions = soup2.find_all('meta', attrs={"content":re.compile("^Joomla.?.")})
                        DRVersions = soup2.find_all('meta', attrs={"content":re.compile("^Drupal.?.")})
                        # Pide respuesta de linkk+/wp-admin/ y si da codigo 200 es que es una web wordpress
                        req2W = requests.get(linkk+"/wp-admin/")
                        # Mejora deteccion wordpress
                        WPThemes = soup2.find_all('link', attrs={"href": re.compile(".?./wp-content/themes/.?.")})
                        # Detector de temas
                        print ""
                        if "WordPress" in strLink or req2W == 200:
                            print link.get('href') + ' - [WORDPRESS]'
                            for WPVersion in WPVersions:
                                WPVersionContent = WPVersion["content"]
                                if str(WPVersionContent) != "WordPress 4.7.4":
                                    print chr(27)+"[0;36m"+"    [*] Version: "+chr(27)+"[0m"
                                    print chr(27)+"[0;36m"+"       - "+WPVersion["content"]+chr(27)+"[0m"+chr(27)+"[6;31m"" [OUTDATED]"+chr(27)+"[0m"
                                else:
                                    print chr(27)+"[0;36m"+"    [*] Version: "+chr(27)+"[0m"
                                    print chr(27)+"[0;36m"+"       - "+WPVersion["content"]+chr(27)+"[0m"
                                if WPThemes:
                                    print chr(27)+"[0;36m"+"    [*] Tema: "+chr(27)+"[0m"
                                    for theme in WPThemes:
                                        themeContent = theme["href"]
                                        print "       - "+themeContent.split("/")[5]
                                        break
                                    break

                        elif "Joomla" in strLink:
                            print link.get('href') + ' - [JOOMLA]'
                            for JOOVersion in JOOVersions:
                                print chr(27)+"[0;36m"+"   - "+JOOVersion["content"]+chr(27)+"[0m"
                        elif "Drupal" in strLink:
                            print link.get('href') + ' - [DRUPAL]'
                            for DRVersion in DRVersions:
                                print chr(27)+"[0;36m"+"    [*] Version: "+chr(27)+"[0m"
                                print chr(27)+"[0;36m"+"       - "+DRVersion["content"]+chr(27)+"[0m"
                            if not DRVersions:
                                print chr(27)+"[0;36m"+"    [*] Version: "+chr(27)+"[0m"
                                print chr(27)+"[0;31m"+"       - No disponible"+chr(27)+"[0m"
                        elif "PrestaShop" in strLink:
                            print link.get('href') + ' - [PRESTASHOP]'
                        else:
                            print chr(27)+"[0;20m"+link.get('href') + ' - [NOCMS]'+chr(27)+"[0m"
                            #print chr(27)+"[0;36m"+"   - "+"Possible SQLi on: "+link.get('href')+"?id=1"+chr(27)+"[0m"

            except requests.exceptions.ConnectionError as error:
                 continue

def main(argv):
    global pagina
    global lugar
    pagina = "1"

    try:
        parser = ArgumentParser()
        parser.add_argument('-p', '--pagina', default="1")
        parser.add_argument('-l', '--lugar')
        args = parser.parse_args()
        pagina = args.pagina
        lugar = args.lugar
        print "[*] Has seleccionado la pagina "+pagina
        print "[*] Has seleccionado el lugar "+lugar
        print "[/] Buscando Webs.. "
        search()
    except TypeError:
        print "Por favor selecciona un lugar: -l, --lugar"
        pass

if __name__ == "__main__":
   main(sys.argv[1:])


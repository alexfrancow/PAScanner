#!/usr/bin/python
from bs4 import BeautifulSoup
import requests
import re
import sys, getopt
# Argumentos https://www.tutorialspoint.com/python/python_command_line_arguments.htm
# Diccionarios http://librosweb.es/libro/python/capitulo_8/metodos_de_retorno.html




def help():
    commands = {
                '-s': 'Indica el tipo de sector (Informatica, Telecomunicaciones..) PROXIMAMENTE',
                '-l': 'Indica el lugar (A Coruna, Barcelona..) PROXIMAMENTE',
                '-p': 'Indica el numero de paginas [1, 2.. (Por defecto 1]',
    }
    for clave, valor in commands.iteritems():
        print (clave, valor)

def search():
    url = 'https://www.paginasamarillas.es/search/informatica/all-ma/a-coru%c3%b1a/all-is/a-coru%c3%b1a/all-ba/all-pu/all-nc/'+ pagina +'?what=informatica&where=A+Coru%C3%B1a'
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')


    #si en url hay 1 haz esto, sino
    if 'https://www.paginasamarillas.es/search/informatica/all-ma/a-coru%C3%B1a/all-is/a-coru%C3%B1a/all-ba/all-pu/all-nc/1?what=informatica&where=A+Coru%C3%B1a' in url:
    #http://stackoverflow.com/questions/3075550/how-can-i-get-href-links-from-html-using-python
    #https://www.crummy.com/software/BeautifulSoup/bs3/documentation.html#arg-attrs
        links = soup.find_all('a', attrs={'itemprop': re.compile("^url")})
        for link in links:
                print link.get('href')

    else:
        links2 = soup.find_all('a')
        for link2 in links2:
                strLink = str(link2)
                if "businessId" in strLink:
                    webs = link2.get('href')
                    req = requests.get(webs)
                    html = req.text
                    soup = BeautifulSoup(html, 'html.parser')
                    links = soup.find_all('a', attrs={'itemprop': re.compile("^url")})
                    for link in links:
                        print link.get('href')


def main(argv):
    global pagina
    pagina = "1"
    try:
        opts, args = getopt.getopt(argv,"h:p:",["pagina=", "help="])
    except getopt.GetoptError:
        print 'test.py -p <pagina>'
        sys.exit(2)
    if not argv:
        print "[*] No has seleccionado pagina"
        print "[/] Buscando webs en la primera.."
        search()
    for opt, arg in opts:
        if opt in ("-h", "-help"):
            help()
            sys.exit()
        elif opt in ("-p", "--pagina"):
            pagina = arg
            print "[*] Has seleccionado la pagina " + str(pagina)
            print "[/] Buscando Webs.. "
            search()

if __name__ == "__main__":
   main(sys.argv[1:])

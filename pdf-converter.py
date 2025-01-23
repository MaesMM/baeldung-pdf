import csv, re, sys, urllib.request
from bs4 import BeautifulSoup, element as bs4Element

def get_html(url):
    opener = urllib.request.URLopener()
    opener.addheader('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0')
    html_path, headers = opener.retrieve(url, "/home/maes/repos/baeldung-pdf/temp.html")
    return html_path

def get_core_content(html_file, delete_hidden=True):
    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    report_container = soup.find('section', {'itemprop': 'articleBody'})
    print(report_container.prettify())
    


def main():
    if len(sys.argv) < 1:
        print("argument : page URL")
        return sys.exit(1)    
    else:
        get_core_content(get_html(sys.argv[1]))

    

if __name__=="__main__":
    main()
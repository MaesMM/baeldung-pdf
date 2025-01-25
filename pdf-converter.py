import os, csv, re, sys, urllib.request
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup, element as bs4Element

dir_path = os.path.dirname(os.path.realpath(__file__))

class Article:
    html_content = ""
    def __init__(self, url):
        self.url = url
        self.type = None
        self.html = self.get_html()

    def get_html(self):
        opener = urllib.request.URLopener()
        opener.addheader('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0')
        html_path, headers = opener.retrieve(self.url, dir_path + "/temp.html")
        return html_path

    def get_type(self):
        types = ['wikipedia', 'baeldung']
        for type in types:
            if type in self.url:
                self.type = type
                break

class ArticleContentHandler(ABC):
    @abstractmethod
    def get_core_content(self, article):
        pass

class BaeldungContentHandler(ArticleContentHandler):
    def get_core_content(self, article):
        with open(article.html, 'r', encoding='utf-8') as file:
            article.html_content = file.read()        
            
        soup = BeautifulSoup(article.html_content, 'html.parser')
        report_container = soup.find('section', {'itemprop': 'articleBody'})
        print(report_container.prettify())


class WikipediaContentHandler(ArticleContentHandler):
    def get_core_content(self, article):
        """BAR"""
        print("Wikipedia article")

def main():
    if len(sys.argv) < 2:
        print("Positional argument needed: <page URL>")
        return sys.exit(1)
    else:
        article = Article(sys.argv[1])
        article.get_type()

        content_handlers = {
            'wikipedia': WikipediaContentHandler(),
            'baeldung': BaeldungContentHandler()
        }

        if article.type in content_handlers:
            content_handlers[article.type].get_core_content(article)
        else:
            print("Unknown article type")

        return sys.exit(0)

if __name__ == "__main__":
    main()

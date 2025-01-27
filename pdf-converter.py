import os, csv, re, sys
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup, element as bs4Element
from urllib import request, parse, error
dir_path = os.path.dirname(os.path.realpath(__file__))

class Article:
    html_content = ""
    def __init__(self, url):
        self.url = url
        self.type = None
        self.html = self.get_html()

    def get_html(self):
        opener = request.URLopener() # Deprecated, use urllib.request.urlopen like in WikipediaContentHandler
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
        parsed_url = parse.urlparse(article.url)
        title = parsed_url.path[1:].replace("/",".")
        with open(title + ".pdf", "w") as file:
            file.write(report_container.prettify())


class WikipediaContentHandler(ArticleContentHandler):
    def get_core_content(self, article):
        parsed_url = parse.urlparse(article.url)
        title = parsed_url.path.split("/")[-1].split("#")[0]
        download_link = "https://en.wikipedia.org/api/rest_v1/page/pdf/" + title
        try:
            with request.urlopen(download_link) as response:
                pdf_content = response.read()
                with open(title + ".pdf", "wb") as file:
                    file.write(pdf_content)
        except error.URLerror as e:
            print(f"Failed to open the download link: {pdf_url}, error: {e}")

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

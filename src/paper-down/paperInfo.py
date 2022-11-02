from typing import List
import requests, re, logging
from bs4 import BeautifulSoup
from thefuzz import fuzz
# import enchant # this is spelling check module
from rich.logging import RichHandler

logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()]
)

class Paper():
    def __init__(self):
        self.name = str
        self.title = List[str]
        self.doi = List[str]
        self.url = List[str]
        self.ref = str,
        self.author = str,
        self.scihub = ['https://sci-hub.ren/','https://sci-hub.yncjkj.com/','https://sci-hub.wf/']
    
    @classmethod
    def get_soup(cls, url:str):
        """get a url return BeautifulSoup

        :param url: url
        :type url: str
        :return: BeautifulSoup
        :rtype: BeautifulSoup
        """
        header = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0"}
        with requests.get(url=url ,headers=header) as res:
            res.encoding = "utf-8"
            html = res.text
            return BeautifulSoup(html, features="lxml")

    def get_paper(self, paper_name:str) :

        self.name = str(paper_name).strip()
        check_lang = "[bold yellow]the word maybe isn't supported[/]"
        if not str(self.name).isascii(): logging.getLogger("get_paper").warning(check_lang, extra={"markup":True})

        url = f"https://www.researchgate.net/search?q={self.name}"
        soup = self.get_soup(url)
        self.title = list(map(lambda i: str(i.string).strip(), soup.select("div.nova-legacy-e-text a.nova-legacy-e-link")))
        self.doi = re.findall(r'DOI\: \<\!-- --\>([^<].*?)\<\/span', str(soup))
        refs = list(zip(self.doi, self.title))
        refs = list(filter(lambda i: fuzz.ratio(str(i[1]).lower() ,str(self.name).lower()) > 80 , refs))
        self.doi = [str(i[0]).replace(r"\/","/") for i in refs]
        self.title = [str(i[1]) for i in refs]
        self.update_scihub()

        return self

    def get_url(self):
            for doi in self.doi:
                for sci in self.scihub:
                    soup = self.get_soup(f"{sci}{doi}")
                    botton = soup.select("#buttons a[onclick]")
                    citation = soup.select("#citation")[0]
                    self.ref = citation.select("i")[0].string.strip()
                    self.author = str(citation.contents[0]).strip()
                    if botton != [] :
                        self.url = re.findall(r"href=\'(.*?)\'", botton[0].attrs["onclick"])
                        self.url = list(map(lambda i: str(i).replace('\/','/'), self.url))
                    if self.url != [] :
                        logging.getLogger("download").info(f"[bold green]downloading:[/] {(self.url)[0]}", extra={"markup":True})
                        break

    
    def update_scihub(self) -> List:
        self.get_url()
        if any(self.url):
            self.get_mirror()
            self.get_url()
            if any(self.url):
                logging.getLogger("get_url").warning("[bold red]download url is blank![/]", extra={"markup": True})
        
        return self.url
            

    def get_mirror(self):
    
        url = ["http://scholar.scqylaw.com/","https://sci-hub.now.sh"]

        def fetch_web(url:str, css:str) -> list:
            soup = self.get_soup(url=url)
            alink = soup.select(css)
            href = list(map(lambda i: i.attrs["href"], alink))
            scihub = list(filter(lambda i: "://sci-hub" in i, href))
            return scihub

        scihub = fetch_web(url=url[0],css="center:nth-of-type(4) ul li a")
        scihub.extend(fetch_web(url=url[1],css=".web .url a.ok"))
        self.scihub = list(set(scihub))

# title = "On Recent Theories and Experiments Regarding Ice at or near Its Melting-Point"
# paper = Paper()
# paper.getPaper(title)

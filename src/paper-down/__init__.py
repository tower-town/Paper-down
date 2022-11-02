from .parse import parse
from .paperInfo import Paper
from .download import download

filename, exportpath = parse()
paper = Paper()
urls = list()
for title in filename:
    info = paper.get_paper(title)
    urls.append(info.url[0])

download(urls, exportpath)
import requests, re
import time
import asyncio
from requests.models import ReadTimeoutError

async def progress_bar(url, path):
    header = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0"}
    path = str(path).replace('\/','/')
    print(repr(path), '\n', url)
    file_name = f'{path}.pdf'
    start = time.time()
    response = requests.get(url=url, headers=header, stream=True)
    size = 0
    chunk_size = 1024
    content_size = int(response.headers['content-length'])
    try:
        if response.status_code != 200:
            for _ in range(5):
                response = requests.get(url=url, headers=header, stream=True)
                content_size = int(response.headers['content-length'])
                if response.status_code == 200:
                    break
        if response.status_code != 200:
            print('maybe invalid  download link')

        if response.status_code == 200:  
            sized = content_size / chunk_size / 1024
            print('Start download,[File size]:{size:.2f} MB'.format(size=sized))
            with open(file_name, 'wb') as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    size += len(data)
                    numstart = int(size * 50 / content_size)
                    rate = float(size / content_size * 100)
                    a = '>'*numstart
                    b = '-'*(50-numstart)
                    print('\r'+'[processing]:%s%s\t%.2f%%' % (a,b, rate), end=' ')

        end = time.time()
        print('Download completed! times: %.2f seconds' % (end - start))

    except Exception as e:
        print('Error!',e,'\n')

async def paper_downing(paper_name,export):

    header = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0"}
    if paper_name == 0:
        pass

    elif '\u4e00' <= paper_name[0] <= '\u9fff':
        print('Chinese_word')

    elif paper_name[0].isalpha():

        paper_name = paper_name.replace(' ', '%20')
        # paper_name.replace(' ', '+')
        url = f'https://www.researchgate.net/search?q={paper_name}'
        res = requests.get(url=url, headers=header, timeout=10)
        res.encoding = 'utf-8'
        html = res.text
        paper_title = re.findall(r'((?<=\"title\":\").*?(?=\",\"doi))', html)

        if paper_title == []:
            print('no find')
        else:
            paper_doi = re.findall(r'((?<=\"doi\":\").*?(?=\",\"isbn\"))', html)
            scihub = ['https://sci-hub.st/','https://sci-hub.ren/']
            for i in range(len(paper_doi)):
                doi = str(paper_doi[i]).replace(r'\/', '/')
                paper_url = scihub[0] + doi
                res_p = requests.get(url=paper_url, headers=header)
                res_p.encoding = 'utf-8'
                paper_txt = res_p.text
                down_url = re.findall(r'(?<=\"location.href=\').*?(?=\'\")', paper_txt)

                if down_url == [] or down_url[1] in scihub:
                    print('\rblank[%d]\t' % i, end='')
                else:
                    if not str(down_url[1]).startswith('https:'):
                        down_url[1] = f'https:{down_url[1]}'
                    if str(down_url[1]).startswith(r'https://moscow'):
                        down_url[1] = str(down_url[1]).replace(r'moscow', 'twin') # twin

                    try:
                        statuscode = requests.get(url=down_url[1], headers=header, timeout=3).status_code
                        if statuscode != 200:
                        # print(f"{paper_title[i]} doi:{doi}")
                            continue
                        print(f"{paper_title[i]} doi:{doi}")
                        exportpath = f"{export}\{paper_title[i]}"
                        task = asyncio.create_task(progress_bar(str(down_url[1]), exportpath,))
                        await task
                        break
                    except ReadTimeoutError:
                        print(statuscode)

                    finally:
                        if statuscode != 200:
                            continue
 
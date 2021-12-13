from asyncio.windows_events import NULL
from os import name
from typing import get_args
import requests, re
import time
import asyncio
import argparse


async def progress_bar(url, path):
    header = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0"}
    path = str(path).replace('\/','/')
    print(path, '\n', url)
    file_name = path + '.pdf'
    start = time.time()  
    response = requests.get(url=url, headers=header, stream=True)
    size = 0    
    chunk_size = 1024  
    content_size = int(response.headers['content-length'])  
    try:
        if response.status_code != 200:
            for i in range(5):
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


async def paper_downing(paper_name):

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
        url = 'https://www.researchgate.net/search?q=' + paper_name
        res = requests.get(url=url, headers=header, timeout=10)
        res.encoding = 'utf-8'
        html = res.text
        paper_title = re.findall(r'((?<=\"title\":\").*?(?=\",\"doi))', html)

        if paper_title == []:
            print('no find')
        elif paper_title != []:
            paper_doi = re.findall(r'((?<=\"doi\":\").*?(?=\",\"isbn\"))', html)
            for i in range(len(paper_doi)):
                doi = str(paper_doi[i]).replace(r'\/', '/')
                scihub = ['https://sci-hub.st/','https://sci-hub.ren/']
                paper_url = scihub[0] + doi
                res_p = requests.get(url=paper_url, headers=header)
                res_p.encoding = 'utf-8'
                paper_txt = res_p.text
                down_url = re.findall(r'(?<=\"location.href=\').*?(?=\'\")', paper_txt)

                if down_url == [] or down_url[1] in scihub:
                    print('\rblank[%d]\t' % i, end='')
                else:
                    if not str(down_url[1]).startswith('https:'):
                        down_url[1] = 'https:' + down_url[1]
                    if str(down_url[1]).startswith(r'https://moscow'):
                        down_url[1] = str(down_url[1]).replace(r'moscow', 'twin') # twin

                    statuscode = requests.get(url=down_url[1], headers=header, timeout=3).status_code
                    if statuscode != 200:
                        # print(f"{paper_title[i]} doi:{doi}")
                        continue
                    else:
                        print(f"{paper_title[i]} doi:{doi}")
                        task = asyncio.create_task(progress_bar(str(down_url[1]), str(paper_title[i])))
                        await task                        
                        break
               

async def main(x1, x2, x3, x4):

    await asyncio.gather(
        paper_downing(x1),
        paper_downing(x2),
        paper_downing(x3),
        paper_downing(x4)
    )

filename = list()
parser = argparse.ArgumentParser()
parser.add_argument('--name','-n',type=str,help='paper title')
parser.add_argument('--path','-p',type=str,help='file of paper list')
args = parser.parse_args()

if args.name ==None and args.path == None:
    raise('at least one parameter of name and path')

if args.path != None:
    with open(str(args.path),mode='r',encoding='utf-8') as file:
        for i in file.readlines():
             if not str(i).startswith('#') and not str(i) == '\n':
                filename.append(str(i).strip())

if args.name != None:
   filename.append(str(args.name).strip())

print(filename)
step = 4
box = [filename[i:i+step] for i in range(0, len(filename), step)]


def gf(a=0, b=0, c=0, d=0):
    return [a, b, c, d]

print('begin')
for bl in box:
    bl = gf(*bl)
    asyncio.run(main(*bl))
print('finish')

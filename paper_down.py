import requests, re
import time
import asyncio


async def progress_bar(url, path):
    header = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0"}

    print(path, '\n', url)
    file_name = path + '.pdf'
    start = time.time()  # 下载开始时间
    response = requests.get(url=url, headers=header, stream=True)
    size = 0    # 初始化已下载大小
    chunk_size = 1024  # 每次下载的数据大小
    content_size = int(response.headers['content-length'])  # 下载文件总大小
    try:
        if response.status_code != 200:
            for i in range(5):
                response = requests.get(url=url, headers=header, stream=True)
                content_size = int(response.headers['content-length'])
                if response.status_code == 200:
                    break
        if response.status_code != 200:
            print('maybe invalid  download link')

        if response.status_code == 200:  # 判断是否响应成功
            sized = content_size / chunk_size / 1024
            # 开始下载，显示下载文件大小
            print('Start download,[File size]:{size:.2f} MB'.format(size=sized))
            with open(file_name, 'wb') as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    size += len(data)
                    numstart = int(size * 50 / content_size)
                    rate = float(size / content_size * 100)
                    a = '>'*numstart
                    b = '-'*(50-numstart)
                    # 显示进度条
                    print('\r'+'[下载进度]:%s%s\t%.2f%%' % (a,b, rate), end=' ')

        end = time.time()   # 下载结束时间
        print('Download completed! times: %.2f秒' % (end - start))  # 输出下载用时时间
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
        # url = 'https://arc.aiaa.org/action/doSearch?AllField=Modal+Synthesis+for+Combined+Structural-Acoustic+Systems%2C'
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
                paper_url = 'https://sci-hub.st/' + doi
                # paper_url = 'https://sci-hub.ren/' + doi
                res_p = requests.get(url=paper_url, headers=header)
                res_p.encoding = 'utf-8'
                paper_txt = res_p.text
                down_url = re.findall(r'(?<=\"location.href=\').*?(?=\'\")', paper_txt)

                if down_url == []:
                    print('\rblank[%d]\t' % i, end='')
                elif down_url != []:
                    # print(str(paper_title[fi]))
                    if not str(down_url[0]).startswith('https:'):
                        down_url[0] = 'https:' + down_url[0]
                    if str(down_url[0]).startswith(r'https://moscow'):
                        ss = str(down_url[0])
                        ss = ss.replace(r'moscow', 'zero')
                        down_url[0] = ss

                    task = asyncio.create_task(progress_bar(str(down_url[0]), str(paper_title[i])))
                    await task
                    # print(str(paper_title[fi]))
                    break


async def main(x1, x2, x3, x4):

    await asyncio.gather(
        paper_downing(x1),
        paper_downing(x2),
        paper_downing(x3),
        paper_downing(x4)
    )

# papper title as list

filename = ['Modal acoustic transfer vector approach in a FEM-BEM vibro-acoustic analysis',
            'Vibroacoustic optimization using a statistical energy analysis model',
            'A finite element method for determining the acoustic modes of irregular shaped cavities',
            'Active sound quality control of engine induced cavity noise']

# with open('down.txt',mode='r',encoding='utf-8') as file:
#     # file.readline()
#     filename.append(file.readline())

step = 4
box = [filename[i:i+step] for i in range(0, len(filename), step)]


def gf(a=0, b=0, c=0, d=0):
    return [a, b, c, d]

print('begin')
for bl in box:
    bl = gf(*bl)
    asyncio.run(main(*bl))
print('finish')

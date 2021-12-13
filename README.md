# paper down

一个简单的论文下载器（目前仅支持英文论文批量下载）

## 版本要求：python 3.7+

目前基于[asyncio --- 异步 I/O ](https://docs.python.org/zh-cn/3/library/asyncio-task.html)

## 第三方库

```bash
 pip install requests
```

## 简单演示/usage

```bash
usage: paper_down.py [-h] (--name NAME | --path PATH) [--export EXPORT]

optional arguments:
  -h, --help                  show this help message and exit
  --name NAME, -n NAME        paper title
  --path PATH, -p PATH        input file of paper list
  --export EXPORT, -e EXPORT  export path of download paper
```
输入论文列表

```vim
# papper title as list # The comment will be ignore.

Modal acoustic transfer vector approach in a FEM-BEM vibro-acoustic analysis
Vibroacoustic optimization using a statistical energy analysis model
A finite element method for determining the acoustic modes of irregular shaped cavities
Active sound quality control of engine induced cavity noise
```

## todo:

- [ ] 添加中文论文下载
- [ ] 添加参考文献元素抓取

# reference

[python 命令行参数](https://tendcode.com/article/python-shell/)
[argparse](https://docs.python.org/zh-cn/3/library/argparse.html)
在下载进度条是参考`CSND`的某一位博主的（具体是谁给忘了）

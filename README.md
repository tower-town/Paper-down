# paper down

一个简单的论文下载器（仅支持英文论文批量下载）

## 版本要求：python 3.7+

// 目前基于[asyncio --- 异步 I/O ](https://docs.python.org/zh-cn/3/library/asyncio-task.html)

## 第三方库

```bash
 poetry install
 
 # for pytest
 poety shell
 pytest

```

## 简单演示/usage

```bash
Usage: test.py [OPTIONS]

  download paper at the command line

mandatary options: [at least 1 required]
  -n, --name <title>   paper title
  -p, --path <path>    input file of paper list

optional:
  -e, --export <path>  export path of download paper (default: current directory)
  --debug BOOLEAN      debug

Other options:
  --help               Show this message and exit.
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

- [x] 添加中文论文下载
- [x] 添加参考文献元素抓取

# reference


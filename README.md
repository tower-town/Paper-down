# paper down

一个简单的论文下载器（目前仅支持英文论文批量下载）

# 版本要求：python 3.7+ 

我只做过python 3.7 和 python 3.8的测试，其他版本没测过。目前基于[asyncio --- 异步 I/O ](https://docs.python.org/zh-cn/3/library/asyncio-task.html)
做的，你也可以不用这个（就是可能在多个论文下载的慢一点而已），就应该没有版本限制吧。

# 第三方库

```bash
 pip install requests
```

# 简单演示

输入论文列表
```bash
    # papper title as list

filename = ['Modal acoustic transfer vector approach in a FEM-BEM vibro-acoustic analysis',
            'Vibroacoustic optimization using a statistical energy analysis model',
            'A finite element method for determining the acoustic modes of irregular shaped cavities',
            'Active sound quality control of engine induced cavity noise']
```
也可以是txt文件，去掉这里的注释并把上面的列表`filename`设为空，保持输入文件和这里的`down.txt`一致，改名字那肯定是可以啊

```bash
# with open('down.txt',mode='r',encoding='utf-8') as file:
#     # file.readline()
#     filename.append(file.readline())
```

# todo:

-[ ] 添加中文论文下载
-[ ] 添加参考文献元素抓取

# reference

在下载进度条是参考`CSND`的某一位博主的（具体是谁给忘了）

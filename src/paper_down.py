
import asyncio
import os
from download import paper_downing
from parse import argument
             

async def main(x1, x2, x3, x4,arg):

    await asyncio.gather(
        paper_downing(x1,arg),
        paper_downing(x2,arg),
        paper_downing(x3,arg),
        paper_downing(x4,arg)
    )

filename,export =argument()
step = 4
box = [filename[i:i+step] for i in range(0, len(filename), step)]


def gf(a=0, b=0, c=0, d=0):
    return [a, b, c, d]

print('begin')
for bl in box:
    bl = gf(*bl)
    asyncio.run(main(*bl,arg=export))
print('finish')

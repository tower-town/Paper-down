
import asyncio
from download import paper_downing
from parse import argument
             

async def main():

    filename,export =argument()
    print('begin')
    for task in filename:
        await asyncio.gather(paper_downing(task,export))
    print('end')

asyncio.run(main())


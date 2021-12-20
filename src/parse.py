import argparse
import os

def argument():
    
    filename = list()
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--name','-n',type=str,help='paper title')
    group.add_argument('--path','-p',type=str,help='input file of paper list')
    parser.add_argument('--export','-e',help='export path of download paper',default=os.path.dirname(str(os.getcwd())))
    args = parser.parse_args()
    exportpath = args.export

    if args.path != None:
        with open(str(args.path),mode='r',encoding='utf-8') as file:
            filename = filter(lambda index :(not (str(index).startswith('#') or str(index) == '\n')),file.readlines())
            
    if args.name != None:
        filename.append(str(args.name).strip())

    return list(filename),exportpath

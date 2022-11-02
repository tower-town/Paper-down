from pathlib import Path
import cloup

formatter_settings = cloup.HelpFormatter.settings(
    max_width = 100,
    theme=cloup.HelpTheme(
        invoked_command=cloup.Style(fg='bright_yellow'),
        heading=cloup.Style(fg='bright_green',bold=True),
        constraint=cloup.Style(fg='magenta'),
        col1=cloup.Style(fg='cyan'),
    )
)

@cloup.command(formatter_settings=formatter_settings)
@cloup.option_group(
    "mandatary options",
    cloup.option('-n','--name', 
                metavar="<title>",
                type=str,
                help='paper title'),
    cloup.option('-p','--path',
                metavar="<path>",
                type=cloup.Path(exists=True,readable=True),
                # default=sys.stdin,
                help='input file of paper list'),
    constraint=cloup.constraints.RequireAtLeast(1),
)


@cloup.option_group(
    "optional",
    cloup.option('-e','--export',
            metavar="<path>",
            type=cloup.dir_path(writable=True,exists=True),
            help='export path of download paper (default: current directory)',
            default=str(Path.cwd().parents[0])),
    cloup.option('--debug',
            help="debug",
            type=bool,
            default=False)
)


def parse(name:str,path:str,export:str, debug:bool) :
    """download paper at the command line"""
    exportpath = export
    filename = list()
    if path != None:
        with open(str(path),mode='r',encoding='utf-8') as file:
            filefilter = filter(lambda index :(not (str(index).startswith('#') or str(index) == '\n')),file.readlines())
            filename = list(filefilter)
            
    if name != None and type(name) == str:
        filename.append(str(name).strip())

    # print(f"{name}\n{path}\n{export}\n{debug}")
    # print(filename, exportpath)
    return filename, exportpath


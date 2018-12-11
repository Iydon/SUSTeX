"""
python texfind.py init
python texfind.py init -d c:/texlive
python texfind.py -c abstract
python texfind.py -e abstract
python texfind alive
"""


import os
import re
import sys


# CONSTANT
DASH      = "-"
DEFAULT   = "default"
INIT      = "init"
DIRECTORY = "d"
ENCODE    = "utf-8"
FILE      = "texlive"
ALIVE     = "alive"
COMMAND   = "c" # 命令
ENVIRON   = "e" # 环境

SUFFIX = [".sty", ".cls"]

# Variables
root      = "C:/texlive"
command   = dict()
environ   = dict()

# Functions

PYOUT = print

def parse_argment(lst:list, result:dict=dict()):
    """
    parse_argment(['texfind.py', '-h', '-f', 'main.tex'])
    =>
    {'h':True, 'f':'main.tex'}
    """
    if lst[0]==__file__: lst=lst[1:]
    length,i = len(lst),0
    while i<length:
        if lst[i][0]==DASH:
            if i+1<length:
                if lst[i+1][0]==DASH:
                    result[lst[i]] = True
                else:
                    result[lst[i]] = lst[i+1]
                    i += 1
            else:
                result[lst[i]] = True
        else:
            result[DEFAULT] = lst[i]
        i += 1
    return result

def remove_dash(obj):
    """
    删除 `-'.
    """
    if isinstance(obj, str):
        return obj.replace(DASH, "")
    elif isinstance(obj, list):
        return [o.replace(DASH, "") for o in obj]
    elif isinstance(obj, dict):
        return dict([[remove_dash(k),remove_dash(v)] for k,v in obj.items()])

def load_file(file, mode="r"):
    """
    载入文件.
    """
    with open(file, "r", encoding=ENCODE, errors="replace") as f:
        return f.read()

def save_file(file, content, mode="w"):
    """
    保存文件.
    """
    with open(file, "w", encoding=ENCODE) as f:
        f.write(content)

def tex_find(opt, name):
    """
    texfind.
    """
    return eval(load_file(FILE+DASH+opt, "r")).get(name, False)

def is_right_suffix(file_name):
    """
    判断后缀名是否合适.
    """
    for s in SUFFIX:
        if file_name.endswith(s):
            return True
    return False

def extract_command(content):
    """
    pass
    """
    pattern = r"(?<=\\%s\\)[^{#]+"
    f = lambda x: re.findall(pattern%x, content)
    return f("def") + f("edef") + f("gdef") + f("newcommand")

def extract_environ(content):
    """
    pass
    """
    pattern = r"(?<=\\newenvironment{)\S+?(?=})"
    return re.findall(pattern, content)


args = {DEFAULT:False, DASH+DIRECTORY:False,
        DASH+COMMAND:False, DASH+ENVIRON:False}
args = parse_argment(sys.argv, args)

if not args[DEFAULT]:
    if args[DASH+COMMAND]:
        result = tex_find(COMMAND, args[DASH+COMMAND])
        PYOUT(result)
    elif args[DASH+ENVIRON]:
        result = tex_find(ENVIRON, args[DASH+ENVIRON])
        PYOUT(result)
    else:
        PYOUT("使用`texfind init'初始化数据库.")
        PYOUT("使用`texfind name'查找提供name的宏包.")
elif args[DEFAULT]==INIT:
    root = args[DASH+DIRECTORY] if args[DASH+DIRECTORY] else root
    for dirpath, dirnames, filenames in os.walk(root):
        for filepath in filenames:
            file_path = os.path.join(dirpath, filepath)
            if is_right_suffix(filepath):
                try:
                    content = load_file(file_path, "r")
                    c_t,e_t = extract_command(content),extract_environ(content)
                    for c in c_t:
                        if c in command:
                            command[c].append(filepath)
                        else:
                            command[c] = [filepath]
                    for e in e_t:
                        if e in environ:
                            environ[e].append(filepath)
                        else:
                            environ[e] = [filepath]
                except Exception as e:
                    PYOUT("Error @ %s: "%file_path)
                    PYOUT("    ", e)
    save_file(FILE+DASH+COMMAND, str(command), "w")
    save_file(FILE+DASH+ENVIRON, str(environ), "w")
elif args[DEFAULT]==ALIVE:
    dc = eval(load_file(FILE+DASH+COMMAND, "r"))
    de = eval(load_file(FILE+DASH+ENVIRON, "r"))
    while True:
        try:
            name = input(">>> ")
        except:
            PYOUT("Bye world.")
            break
        PYOUT("Command: ")
        PYOUT(dc.get(name, False))
        PYOUT()
        PYOUT("Environment: ")
        PYOUT(de.get(name, False))
        PYOUT()
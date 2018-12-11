"""
python texfind.py init
python texfind.py init -d c:/texlive
python texfind.py -c abstract
python texfind.py -e abstract
python texfind.py -p mcmthesis
python texfind alive
"""


import os
import re
import sys


# CONSTANT
DASH      = "-"
LINEBR    = "\n"
DEFAULT   = "default"
INIT      = "init"
ENCODE    = "utf-8"
FILE      = "texlive"
DIRECTORY = "d"       # 指定初始化路径
COMMAND   = "c"       # 查找命令定义宏包
ENVIRON   = "e"       # 查找环境定义宏包
PACKAGE   = "p"       # 朝赵宏包文类依赖
ALIVE     = "alive"   # 保持查询状态

SUFFIX = [".sty", ".cls"]

# Variables
root      = "C:/texlive"
command   = dict()
environ   = dict()
package   = dict()

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
    return LINEBR.join(eval(load_file(FILE+DASH+opt, "r")).get(name, ["None"]))

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
    提取定义命令.
    """
    pattern = r"(?<=\\%s\\)[^{#]+"
    f = lambda x: re.findall(pattern%x, content)
    return f("def") + f("edef") + f("gdef") + f("newcommand")

def extract_environ(content):
    """
    提取定义环境.
    """
    pattern = r"(?<=\\newenvironment{)\S+?(?=})"
    return re.findall(pattern, content)

def extract_package(content, file_name):
    """
    提取使用宏包.
    """
    MatchBeforeAndAfter = "(?<=%s)%s(?=%s)"
    MatchWithout = "[^%s]%s"
    MatchWith    = "[%s]%s"
    SPACE   = " "
    ESCAPE  = "\\\\"
    OPTIONS = [r"\[", r"\]"]
    GROUP   = ["{", "}"]
    PROVIDE = ["ProvidesPackage", "ProvidesClass", "ProvidesFile"]
    REQUIRE = ["RequirePackage", "usepackage"]
    def remove_comment(string:str):
        pattern = "%s%s%s"%("%", MatchWithout%(LINEBR,"*"), LINEBR)
        pattern = "%[^\n]*\n"
        return re.sub(pattern, LINEBR, string)
    def remove_space(string:str):
        pattern = MatchWith%(SPACE+LINEBR, "*")
        return re.sub(pattern, "", string)
    def remove_option(string:str):
        pattern = "%s%s%s"%(OPTIONS[0], r"\S*?", OPTIONS[-1])
        return re.sub(pattern, "", string)
    def extract_group(string:str, opt:list):
        result = []
        for o in opt:
            pattern = MatchWithout%(GROUP[-1]+ESCAPE, "*")
            pattern = "%s%s%s%s"%(o, GROUP[0], pattern, GROUP[-1])
            result += re.findall(pattern, string)
        return result
    def extract_content_in_line(string:str):
        pattern = MatchBeforeAndAfter%(GROUP[0], MatchWithout%(GROUP[-1], "*"), GROUP[-1])
        result  = re.findall(pattern, string)
        return result[0].split(",")
    def extract_content(lst:list):
        result = []
        for item in lst:
            result += extract_content_in_line(item)
        return result
    content = remove_option(remove_space(remove_comment(content)))
    require = extract_content(extract_group(content, REQUIRE))
    provide = extract_content(extract_group(content, PROVIDE))
    if provide:
    	provide = os.path.splitext(provide[0])[0]
    else:
    	provide = os.path.splitext(file_name)[0]
    return provide,require


args = {DEFAULT:False,
        DASH+DIRECTORY:False,
        DASH+COMMAND:False,
        DASH+ENVIRON:False,
        DASH+PACKAGE:False,}
args = parse_argment(sys.argv, args)

if not args[DEFAULT]:
    if args[DASH+COMMAND]:
        result = tex_find(COMMAND, args[DASH+COMMAND])
        PYOUT(result)
    elif args[DASH+ENVIRON]:
        result = tex_find(ENVIRON, args[DASH+ENVIRON])
        PYOUT(result)
    elif args[DASH+PACKAGE]:
        result = tex_find(PACKAGE, args[DASH+PACKAGE])
        PYOUT(result)
    else:
        PYOUT("使用`texfind init'初始化数据库.")
        PYOUT("使用`texfind alive'保持查询状态.")
elif args[DEFAULT]==INIT:
    root = args[DASH+DIRECTORY] if args[DASH+DIRECTORY] else root
    for dirpath, dirnames, filenames in os.walk(root):
        for filepath in filenames:
            file_path = os.path.join(dirpath, filepath)
            if is_right_suffix(filepath):
                try:
                    content = load_file(file_path, "r")
                    c_t = extract_command(content)
                    e_t = extract_environ(content)
                    p_t = extract_package(content, filepath)
                    package[p_t[0]] = p_t[-1]
                    for c in c_t:
                        if c in command:
                            command[c].append(file_path)
                        else:
                            command[c] = [file_path]
                    for e in e_t:
                        if e in environ:
                            environ[e].append(file_path)
                        else:
                            environ[e] = [file_path]
                except Exception as e:
                    PYOUT("Error @ %s: "%file_path)
                    PYOUT("    ", e)
    save_file(FILE+DASH+COMMAND, str(command), "w")
    save_file(FILE+DASH+ENVIRON, str(environ), "w")
    save_file(FILE+DASH+PACKAGE, str(package), "w")
elif args[DEFAULT]==ALIVE:
    dc = eval(load_file(FILE+DASH+COMMAND, "r"))
    de = eval(load_file(FILE+DASH+ENVIRON, "r"))
    dp = eval(load_file(FILE+DASH+PACKAGE, "r"))
    while True:
        try:
            name = input(">>> ")
        except:
            PYOUT("Bye world.")
            break
        PYOUT("Command: ")
        PYOUT(LINEBR.join(dc.get(name, ["None"])))
        PYOUT()
        PYOUT("Environment: ")
        PYOUT(LINEBR.join(de.get(name, ["None"])))
        PYOUT()
        PYOUT("Packages: ")
        PYOUT(", ".join(dp.get(name, ["None"])))
        PYOUT()
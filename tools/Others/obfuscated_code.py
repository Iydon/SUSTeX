import os
import random
import re
import sys


# Function(s)
def init():
    # Variables
    root    = "C:/texlive"
    ext     = [".sty", ".cls", ".tex"]
    encode  = "utf-8"
    file    = "comments"
    pattern = "\n%[^\n]+"
    # body
    for dirpath, dirnames, filenames in os.walk(root):
        for filepath in filenames:
            file_path = os.path.join(dirpath, filepath)
            if any([filepath.endswith(e) for e in ext]):
                with open(file_path, "r", encoding=encode, errors="replace") as f:
                    result = re.findall(pattern, f.read())
                with open(file, "a+", encoding=encode) as f:
                    f.write("".join(result))
                # print(file_path)


def input_include(content:str):
    in_  = ["\\\\input{[^}]+}", "\\\\include{[^}]+}"]
    out_ = ["(?<=\\\\input{)[^}]+?(?=})", "(?<=\\\\include{)[^}]+?(?=})"]
    content_ = content
    encode   = "utf-8"
    tex      = ".tex"
    if any([re.findall(i, content) for i in in_]):
        for i in range(len(in_)):
            for part in re.findall(in_[i], content):
                part = part.replace("\\", r"\\")
                file = re.findall(out_[i], content)[0]
                file = file if file.endswith(tex) else file+tex
                try:
                    with open(file, "r", encoding=encode) as f:
                        content_ = re.sub(part, f.read(), content_, count=1)
                except:
                    continue
        for line in content_.splitlines():
            yield line + "\n"
    else:
        yield content


def add_comments(file_name:str):
    file   = "comments"
    encode = "utf-8"
    output = "_%s"%file_name
    num    = 128
    with open(file, "r", encoding=encode) as f:
        content = f.readlines()
        length  = len(content)
    os.system("echo %% > %s"%output)
    with open(file_name, "r", encoding=encode) as f:
        with open(output, "a+", encoding=encode) as g:
            for line in f.readlines():
                for item in input_include(line):
                    g.write("".join(random.choices(content, k=random.randint(0,num))))
                    g.write(item)
            g.write("".join([i.replace("%","") for i in random.choices(content, k=random.randint(0,num))]))

# Initialize
# init()


if sys.argv[1:]:
    file = sys.argv[1]
else:
    file = "demo.tex"
add_comments(file)

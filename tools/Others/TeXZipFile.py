import os
import re
import rstr
import sys


# Constant(s)
ERROR    = ["\n!"]
WARNING  = ["No file [^\n]+aux", "Warning"]
BADBOX   = ["Overfull"]
MAIN     = ["(^|\n)[^%\n]+documentclass"]
COMPILER = ["pdftex", "xetex", "luatex", "pdflatex", "xelatex", "lualatex"]
ENCODE   = "utf-8"
TMPDIR   = "tmp%s"%rstr.xeger("[a-zA-Z0-9]{16}")
CD       = "cd %s"
AND      = " && "

# Extension
LOG      = ".log"
TEX      = ".tex"
ZIP      = {
             ".zip": "unzip -d %s %%s"%TMPDIR,
             ".7z":  "7z e %%s -r -o%s"%TMPDIR,
           }

# Compiler(s)
PDFTEX   = "pdflatex -shell-escape -halt-on-error %s"
XETEX    = "xelatex  -shell-escape -halt-on-error %s"
LUATEX   = "lualatex -shell-escape -halt-on-error %s"

# Variable(s)
file = "demo.zip"
flag = False


# Function(s)
def count(content:str, PATTERN:list) -> int:
    """
    Count the number of pattern(s).
    """
    return sum([len(re.findall(P, content)) for P in PATTERN])

def count_error(content:str, ERROR:list=ERROR) -> int:
    """ Count the number of error(s). """
    return count(content, ERROR)

def count_warning(content:str, WARNING:list=WARNING) -> int:
    """ Count the number of warning(s). """
    return count(content, WARNING)

def count_badbox(content:str, BADBOX:list=BADBOX) -> int:
    """ Count the number of badbox(es). """
    return count(content, BADBOX)

def extract_compiler(content:str, COMPILER:list=COMPILER) -> str:
    """ Extract whether the compiler use. """
    result = re.findall("|".join(COMPILER), content.lower())
    if result:
        if "pdf" in result[0]:
            return PDFTEX
        elif "xe" in result[0]:
            return XETEX
        elif "lua" in result[0]:
            return LUATEX
    return XETEX

def is_main(content:str, MAIN:str=MAIN) -> bool:
    """
    Judge whether the content is main.
    """
    for M in MAIN:
        if not re.findall(M, content):
            return False
    return True

def clear(TMPDIR:str=TMPDIR):
    """
    Clear the temp file.
    """
    cmd = [ "del /q %s"%TMPDIR,
            "rmdir %s"%TMPDIR, ]
    for c in cmd:
        os.system(c)


if sys.argv[1:]:
    file = sys.argv[1]

if file.endswith(TEX):
    # TODO
    with open(file, "r", encoding=ENCODE) as f:
        content = f.read()
        cmd = extract_compiler(content)
        pass
else:
    for Z in ZIP:
        if file.endswith(Z):
            os.system(ZIP[Z]%file)
            for dirpath, dirnames, filenames in os.walk(TMPDIR):
                for filepath in filenames:
                    file_path = os.path.join(dirpath, filepath)
                    if file_path.endswith(TEX):
                        with open(file_path, "r", encoding=ENCODE, errors="replace") as f:
                            content = f.read()
                            if is_main(content):
                                print(dirpath)
                                cmd = extract_compiler(content)
                                os.system(AND.join([CD%dirpath, cmd%filepath]))
                                flag = True
                    if flag:
                        break
                if flag:
                    break
            log_file = file_path.split(".")[0] + LOG
            col,row = os.get_terminal_size()
            print("\n"*row)
            with open(log_file, "r", encoding=ENCODE) as f:
                content = f.read()
                if count_error(content):
                    print("Compile failed.")
                else:
                    print("Compiled successfully.")
                    print("Warning(s):", count_warning(content))
                    print("Bad Box(s):", count_badbox(content))
            continue


# Clear temp file.
if input("Delete(Y/N)? ").lower()=="n":
    pass
else:
    clear()

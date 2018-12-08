import argparse
import os
import re

# Content
NAME       = "Coding"
DESCRIP    = "转码工具."
RECURSIVE  = "是否遍历文件夹下所有文件, 默认为`否'."
DIRECTORY  = "目标文件夹, 默认为当前目录下."
IDENTIFIER = "分隔符, 默认为逗号`.'"
SUFFIX     = "后缀, 默认为`.tex'."
FROM       = "转码最初编码名称, 默认为`GBK'."
TO         = "编码目标编码名称, 默认为`UTF-8'."

# New parser
parser = argparse.ArgumentParser()
parser.description = DESCRIP

# Add argument
# python coding -r 0 -d "./" -i , -s .tex,.sty.cls -f from -t to
# python coding -d README.md
parser.add_argument("-v", "--Version", action="version", version="%s 0.1"%NAME)
parser.add_argument("-r", "--Recursive",  type=str, help=RECURSIVE)
parser.add_argument("-d", "--Directory",  type=str, help=DIRECTORY)
parser.add_argument("-i", "--Identifier", type=str, help=IDENTIFIER)
parser.add_argument("-s", "--Suffix",     type=str, help=SUFFIX)
parser.add_argument("-f", "--From",       type=str, help=FROM)
parser.add_argument("-t", "--To",         type=str, help=TO)

# Args
args = parser.parse_args()

# Default parameter
if args.Recursive==None:  args.Recursive="0"
if args.Directory==None:  args.Directory="."
if args.Identifier==None: args.Identifier=","
if args.Suffix==None:     args.Suffix=".tex"
if args.From==None:       args.From="gbk"
if args.To==None:         args.To="utf-8"

# Functions
PYOUT = print

def is_right_suffix(name:str, suffix:str, identifier:str):
	"""
	判断后缀名是否需要更改.
	-------
	Args:
	    name:       String, 文件名称.
	    suffix:     String, 命令行输入后缀.
	    identifier: String, 分隔符, 生成后缀列表.
	"""
    for i in suffix.split(identifier):
        if name.endswith(i):
            return True
    return False

def change_coding(File:str, From:str, To:str):
	"""
	更改编码.
	-------
	Args:
	    File: String, 文件名称.
	    From: String, 初始编码.
	    To:   String, 目标编码.
	"""
    content = b""
    with open(File, "rb") as f:
        content = f.read()
    with open(File, "wb") as f:
        try:
            f.write(content.decode(From).encode(To))
        except Exception as e:
            f.write(content)
            PYOUT("Error @ %s"%File)
            PYOUT(e, "\n")
    with open("%s~"%File, "wb") as f:
        f.write(content)

if args.Recursive == "1":
	# 递归更改文件.
    for dirpath, dirnames, filenames in os.walk(args.Directory):
        for filepath in filenames:
            file_path = os.path.join(dirpath, filepath)
            # 更改特定后缀文件.
            if is_right_suffix(file_path, args.Suffix, args.Identifier):
                change_coding(file_path, args.From, args.To)
elif args.Recursive == "0":
	# 当前文件夹.
    for file in os.listdir(args.Directory):
        file_path = os.path.join(args.Directory, file)
        if os.path.isdir(file_path):
            continue
        # 更改特定后缀文件.
        if is_right_suffix(file_path, args.Suffix, args.Identifier):
            change_coding(file_path, args.From, args.To)
else:
	# 指定文件.
    if is_right_suffix(args.Recursive, args.Suffix, args.Identifier):
        change_coding(args.Recursive, args.From, args.To)
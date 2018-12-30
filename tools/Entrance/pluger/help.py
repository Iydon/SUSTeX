import re


FILE   = "data.tsv"
ENCODE = "utf-8"


def read_database(file:str=FILE, encode:str=ENCODE, re:object=re):
    """
    读取数据库, 并且将数据库有用的内容提取成``list''形式.
    """
    # 常量
    TAB     = "\t"
    READ    = "r"
    COMMENT = "#"
    PATTERN = "%s+"%TAB
    # 方法
    def is_text_useful(text, comment:str=COMMENT):
        """
        判断内容是否有用.
        -----------------------
        规则:
            1. 不为空行.
            2. 开头不为``#''.
        返回:
            如果满足空格返回``True'',
            否则返回``False''.
        """
        if text=="":
            return False
        if text[0]==COMMENT:
            return False
        return True
    # 读取文件
    with open(file, READ, encoding=encode) as f:
        data = f.read().splitlines()
    # 删除无用内容
    for i in range(len(data)-1, -1, -1):
        if not is_text_useful(data[i]):
            del data[i]
        else:
            data[i] = re.split(PATTERN, data[i])
    # 返回数据
    return data


def main(text:str):
    data = read_database(FILE, ENCODE, re)
    return "\n".join([", ".join(d[:-1]) for d in data])

import re


# Constant(s)
DATABASE = "data.tsv"
NOTHING  = None
ENCODE   = "utf-8"
PYOUT    = print
EXIT     = "exit"
BYE      = "Bye, world!"


# Function(s)
def read_database(file:str=DATABASE, encode:str=ENCODE, re:object=re):
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


def decide_return(database:list, text:str, case_sensitive:bool=True):
    """
    根据数据库及得到的内容觉得返回的内容.
    """
    # 常量
    SLASH = "/"
    # 方法
    def judge(reference:str, text:str, case:bool=case_sensitive, others:bool=True):
        """
        判断是否满足返回的条件.
        -----------------------
        规则:
            1. 得到的内容包含参考内容.
        返回:
            如果满足条件, 返回``True'',
            否则返回``False''.
        提示:
            如果不注意大小写, 可以在字符串后加``.lower()''.
        """
        f = lambda x: x if case else x.lower()
        return (f(reference) in f(text)) and others
    def is_return(data:list, text:str, slash:str=SLASH):
        """
        判断是否返回.
        -----------------------
        规则:
            1. 所有关键词都满足.
            2. 每个关键词如果以``/''隔开, 则如果其中一个满足即可.
        返回:
            如果满足条件, 返回``True'',
            否则返回``False''.
        """
        length = len(data)
        flag   = [True for i in range(length)]
        for i in range(length):
            if slash in data[i]:
                flag[i] = any([judge(k,text) for k in data[i].split(slash)])
            else:
                flag[i] = judge(data[i], text)
        return all(flag)
    # 遍历数据库, 构造迭代器返回.
    for data in database:
        if is_return(data[:-1], text):
            yield data[-1]


def functional(text:str, ret:str):
    """
    如果为功能性语句, 返回特定功能执行后的结果.
    """
    # 常量
    COLON  = ":"
    PLUG   = "pluger"
    IMPORT = "import %s.%%s"%PLUG
    EVAL   = "%s.%%s.main"%PLUG
    # 方法
    def is_functional(ret:str, colon:str=COLON):
        """
        判断是否满足功能性语句的条件.
        -----------------------
        规则:
            1. 得到的内容包含``:''.
        返回:
            如果满足条件, 返回``True'',
            否则返回``False''.
        """
        if ret:
            return ret[0]==colon
        else:
            return False
    # 导入功能
    if is_functional(ret, COLON):
        exec(IMPORT%ret[1:])
        return eval(EVAL%ret[1:])(text)
    else:
        return ret

data = read_database(DATABASE, ENCODE, re)
while True:
    content = input(">>> ")
    if content==EXIT:
        PYOUT(BYE)
        break
    for item in decide_return(data, content, case_sensitive=True):
        result = functional(content, item)
        if result:
            PYOUT(result)

"""
<<lshort-zh>>, Page 90.
|---------|-----------------|--------|
|   命令   |      样式      |   备注   |
|---------|-----------------|--------|
|arabic   | 阿拉伯数字(默认) |         |
|alph     | 小写字母         |限0-26  |
|Alph     | 大写字母         |限0-26  |
|roman    | 小写罗马数字     |限正数   |
|Roman    | 大写罗马数字     |限正数   |
|fnsymbol | TODO            |限0-9   |
|---------|-----------------|--------|
"""


def arabic(num:int) -> str:
    """
    阿拉伯数字.
    -------------
    Arg(s):
        num: Integer.

    Return(s):
        String.
    """
    return str(num)


def alph(num:int) -> str:
    """
    小写字母.
    -------------
    Arg(s):
        num: Integer.

    Return(s):
        String.
    """
    if num not in range(27):
        raise ValueError("math domain error.")
    return chr(96+num) if num else ""


def Alph(num:int) -> str:
    """
    大写字母.
    -------------
    Arg(s):
        num: Integer.

    Return(s):
        String.
    """
    if num not in range(27):
        raise ValueError("math domain error.")
    return chr(64+num) if num else ""


def roman(num:int) -> str:
    """
    小写罗马数字.
    -------------
    Arg(s):
        num: Integer.

    Return(s):
        String.
    """
    if not isinstance(num,int) or num<=0:
        raise ValueError("math domain error.")
    return Roman(num).lower()


def Roman(num:int) -> str:
    """
    大写罗马数字.
    -------------
    Arg(s):
        num: Integer.

    Return(s):
        String.
    """
    if not isinstance(num,int) or num<=0:
        raise ValueError("math domain error.")
    lnum = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    lstr = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    res  = ""
    for i in range(len(lnum)):
        while num >= lnum[i]:
            num   -= lnum[i]
            res   += lstr[i]
    return res

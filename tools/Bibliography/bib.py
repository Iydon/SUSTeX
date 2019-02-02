import json


def bibtex_parser(string:str):
    """
    Bibtex parser.
    """
    TYPE   = "type"
    LABEL  = "label"
    INFOR  = "information"

    SPACE  = " \t\n"
    ALPHA  = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    NUMBE  = "0123456789"
    DELIM  = {"{":"}", "\"":"\""}

    def tokens(string:str):
        """
        Extract the tokens.
        =========
        Flags:
            1: type
            2: label
            3: key
            4: value
        """
        start,end = 0,0
        stack  = list()
        length = len(string)
        while start < length:
            yield string[start]
            start += 1

    result = list()
    items  = dict()

    for token in tokens(string):
        print(token, end="")

    return result


with open("bib.bib", "r") as f:
    con = f.read()

lst = bibtex_parser(con)
js = [json.dumps(l, sort_keys=True, indent=4, separators=(",",":")) for l in lst]
print(js)

import json


class bib(object):
    """
    Bibtex parser.
    """
    # Constants
    AT  = "@"
    LBR = "{"
    RBR = "}"
    # Variables
    result = list()
    item   = dict()
    # Functions
    def __init__(self, content:str=""):
        self.content = content
        self.length  = len(content)

    def __dir__(self):
        return ["parse", "self_parse", "as_json", "self_as_json"]

    def parse(self, content:str):
        """
        Parse bib content to dict.
        =========
        [{...}, {...}]
        """
        return self.__analysis_item(content)

    def self_parse(self):
        """
        Parse self.
        """
        self.result = list()
        for i in self.__split_items():
            item = self.parse(i)
            self.result.append(item)
        return self.result

    def as_json(self, content:str):
        """
        Parse dict to json.
        =========
        {
            ...
        }
        """
        args = {
            "separators": (",", ":"),
            "sort_keys": True,
            "indent": 4
        }
        return json.dumps(content, **args)

    def self_as_json(self):
        """
        Parse self.
        """
        return [self.as_json(i) for i in self.result]

    def __split_items(self):
        """
        Split items in bib file.
        =========
        @article{ ... }
        """
        start,end = 0,0
        stack = list()
        temp  = str()
        while start < self.length:
            if self.content[start] == self.AT:
                while self.content[end] != self.LBR:
                    end += 1
                stack.append(self.LBR)
                while stack:
                    end += 1
                    if self.content[end] == self.LBR:
                        stack.append(self.LBR)
                    elif self.content[end] == self.RBR:
                        temp = stack.pop()
                        if temp != self.LBR:
                            raise SyntaxError("invalid syntax")
                yield self.content[start:end+1]
                start = end
            else:
                start += 1
                end += 1

    def __analysis_item(self, item:str):
        return {"type":"article", "label":"aqwertyuiop",
                "information": {"a":1, "b":2, "c":3}}



with open("bib.bib", "r") as f:
    con = f.read()

b = bib(con)
print(b.self_parse())
print(b.self_as_json())

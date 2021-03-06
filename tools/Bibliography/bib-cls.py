import json


class bib(object):
    """
    Bibtex parser.
    """
    # Constants
    AT  = "@"
    LBR = "{"
    RBR = "}"
    SPA = " \t\n"
    COM = ","
    TYPE  = "type"
    LABEL = "label"
    INFO  = "information"
    # Variables
    result = list()
    item   = dict()
    # Functions
    def __init__(self, content:str=""):
        self.content = content

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
        return self.as_json(self.result)

    def __split_items(self):
        """
        Split items in bib file.
        =========
        @article{ ... }
        """
        start,end = 0,0
        stack = list()
        temp  = str()
        while start < len(self.content):
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
        """
        Analysis elements in bib item.
        """
        result = {self.TYPE:"", self.LABEL:"", self.INFO:dict()}
        start,end = 0,0
        # Type
        while item[end+1].isalpha():
            end += 1
        result[self.TYPE] = item[start+1:end+1]
        start = end+1
        # Label
        while item[start+1] in self.SPA:
            start += 1
        end = start+1
        while item[end] not in self.SPA+self.COM:
            end += 1
        result[self.LABEL] = item[start+1:end]
        start = end+1
        # Information
        def split(content):
            start,mid,end = 0,0,0
            idx = 0
            stack = list()
            temp  = str()
            while start < len(content):
                if content[start].isalpha():
                    while content[mid].isalpha():
                        mid += 1
                    while content[end] != self.LBR:
                        end += 1
                    stack.append(self.LBR)
                    while stack:
                        end += 1
                        if content[end] == self.LBR:
                            stack.append(self.LBR)
                        elif content[end] == self.RBR:
                            temp = stack.pop()
                            if temp != self.LBR:
                                raise SyntaxError("invalid syntax")
                    idx = content[mid:end+1].index(self.LBR)
                    yield content[start:mid],content[mid+idx:end+1]
                    start = end
                    mid = end
                else:
                    start += 1
                    mid += 1
                    end += 1
        for i,j in split(item[start:-1]):
            result[self.INFO][i] = j[1:-1]
        return result



with open("bib.bib", "r") as f:
    con = f.read()

b = bib(con)
print(b.self_parse())

with open("bib.json", "w") as f:
    f.write(b.self_as_json())

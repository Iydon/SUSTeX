#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/12/27 16:32
# @Author   : Iydon
# @File     : string_transform.py


class string_transform(object):
    r"""
    String transformation.
    ----------
    \RequirePackage{graphicx}
    """

    def __init__(self, string:str):
        """
        Initialize.
        """
        self.tokens = list(string)
        self.length = len(string)

    def __str__(self):
        """
        Return str(self).
        """
        return "".join(self.tokens)


    def rotatebox(self, key=None, pattern=None) -> bool:
        """
        Rotate.
        ----------
        Arg(s):
            key: Lambda function with one
                 parameter.

        Return(s):
            True.
        """
        # default parameters
        if key==None:
            key = lambda x: 0
        if pattern==None:
            pattern = r"\rotatebox[origin=c]{%s}{%s}"
        # body
        self.tokens = [pattern%(key(t),t) for t in self.tokens]
        # return
        return True

    def raisebox(self, unit="ex", key=None, pattern=None) -> bool:
        """
        Raise.
        ----------
        Arg(s):
            unit: String.
            key:  Lambda function with one
                  parameter.

        Return(s):
            True.
        """
        # default parameters
        if key==None:
            key = lambda x: 0
        if pattern==None:
            pattern = r"\raisebox{%%s%s}{%%s}"%unit
        # body
        self.tokens = [pattern%(key(t),t) for t in self.tokens]
        # return
        return True

    def reflectbox(self, key=None, pattern=None) -> bool:
        """
        Reflect.
        ----------
        Arg(s):
            unit: String.
            key:  Lambda function with one
                  parameter.

        Return(s):
            True.
        """
        # default parameters
        if key==None:
            key = lambda x: False
        if pattern==None:
            pattern = r"\reflectbox{%s}"
        # body
        self.tokens = [(pattern%t if key(t) else t) for t in self.tokens]
        # return
        return True

    def scalebox(self, key=None, pattern=None) -> bool:
        """
        Scale.
        ----------
        Arg(s):
            key:  Lambda function with one
                  parameter.

        Return(s):
            True.
        """
        # default parameters
        if key==None:
            key = lambda x: 1
        if pattern==None:
            pattern = r"\scalebox{%s}[%s]{%s}"
        # body
        temp = None
        for i in range(self.length):
            temp = key(self.tokens[i])
            if isinstance(temp, (list,tuple)):
                if len(temp)<1:
                    temp = (1, 1)
                elif len(temp)<2:
                    temp = (temp[0], temp[0])
                else:
                    temp = temp[:2]
            else:
                temp = (temp, temp)
            self.tokens[i] = pattern%(*temp, self.tokens[i])
        # return
        return True

    def resizebox(self, unit="ex", key=None, pattern=None) -> bool:
        """
        Resize.
        ----------
        Arg(s):
            key:  Lambda function with one
                  parameter.

        Return(s):
            True.
        """
        # default parameters
        if key==None:
            key = lambda x: 1
        if pattern==None:
            pattern = r"\resizebox{%s}{%s}{%s}"
        default = "!"
        # body
        for i in range(self.length):
            temp = key(self.tokens[i])
            if isinstance(temp, (list,tuple)):
                if len(temp)<1:
                    temp = (1, 1)
                elif len(temp)<2:
                    temp = (temp[0], 0)
                else:
                    temp = temp[:2]
            else:
                temp = (temp, 0)
            f = lambda x: [("%s%s"%(x,unit) if x else default) for x in x]
            self.tokens[i] = pattern%(*f(temp), self.tokens[i])
        # return
        return True



import random


string = "Happy New Year"
st = string_transform(string)
st.reflectbox(key=lambda x: random.randint(0,1))
print(st)

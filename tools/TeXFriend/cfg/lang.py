#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/11/30
# @Author   : Iydon
# @File     : lang.py


import re
from cfg import cfg


def parse(string:str) -> dict:
    return dict( \
        map(lambda x: re.split("%s *"%cfg.LANG_COLON_IDENTIFIER, x.strip(), maxsplit=1), \
            filter(lambda x: x[0]!=cfg.LANG_COMMENT_IDENTIFIER, \
                string.split(cfg.LANG_LINE_BREAK))))


en = parse("""
# Menubar
    File:        File
    Setting:     Setting
    Help:        Help
# Menubar -> File
    New:         New
    Open:        Open
    Save:        Save
    Exit:        Exit
# Menubar -> Setting
    TopLevel:    Top Level
    WelcomePage: Welcome Page
    Language:    Language
    FontChoose:  Font Choose
# Menubar -> Help
    About:       About
        AboutInformation: TeX Friend, written by Iydon Leong, SUSTeX.
""".strip())

zh = parse("""
# Menubar
    File:        文件
    Setting:     设置
    Help:        帮助
# Menubar -> File
    New:         新建
    Open:        打开
    Save:        保存
    Exit:        退出
# Menubar -> Setting
    TopLevel:    总在最前
    WelcomePage: 显示欢迎页
    Language:    Language
    FontChoose:  字体选择
# Menubar -> Help
    About:       关于
        AboutInformation: TeX Friend, written by Iydon Leong, SUSTeX.
""".strip())

fr = parse("""
# Menubar
    File:        Fichier
    Setting:     Réglage
    Help:        Aide
# Menubar -> File
    New:         Nouveau
    Open:        Ouvert
    Save:        Enregistrer
    Exit:        Sortie
# Menubar -> Setting
    TopLevel:    Toujours au Top
    WelcomePage: Page d'accueil
    Language:    Langue
    FontChoose:  Sélection de Polices
# Menubar -> Help
    About:       À propos de moi
        AboutInformation: TeX Friend, written by Iydon Leong, SUSTeX.
""".strip())

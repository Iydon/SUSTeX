#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/11/30
# @Author   : Iydon
# @File     : lang.py


import re
from cfg import cfg


def parse(string:str) -> dict:
	return dict( \
		map(lambda x: re.split("%s *"%cfg.LANG_COLON_IDENTIFIER, x), \
			filter(lambda x: x[0]!=cfg.LANG_COMMENT_IDENTIFIER, \
				string.split(cfg.LANG_LINE_BREAK))))


en = parse("""
# Menubar
File:     File
Setting:  Setting
Help:     Help
# Menubar -> File
Open:     Open
Save:     Save
New:      New
Exit:     Exit
# Menubar -> Setting
TopLevel: Top Level
Language: Language
""".strip())

zh = parse("""
# Menubar
File:     文件
Setting:  设置
Help:     帮助
# Menubar -> File
Open:     打开
Save:     保存
New:      新建
Exit:     退出
# Menubar -> Setting
TopLevel: 总在最前
Language: Language
""".strip())

fr = parse("""
# Menubar
File:     Fichier
Setting:  Réglage
Help:     Aide
# Menubar -> File
Open:     Ouvrir
Save:     Enregistrer
New:      Nouveau
Exit:     Sortie
# Menubar -> Setting
TopLevel: Haut Niveau
Language: Language
""".strip())
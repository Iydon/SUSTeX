r"""
\def\hello[\guest,\host={Iydon}]{Hello \guest, my name is \host.}
\section{Section}
\subsection{Subsection}
\subsubsection{Subsubsection}
\includegraphics[width=1in]{AVATAR.jpg}
\begin{document}\end{document}

\newpage
\input
"""

import re
from docx import Document
from docx.shared import Inches
from docx.shared import RGBColor
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.text.run import Font


# Constant(s)
FILE    = "demo.tex"
ENCODE  = "utf-8"
ESCAPE  = "\\"
LINEBK  = "\n"
SPACE   = " "
COMMAND = "[a-zA-Z0-9]"

# Function(s)
def read_file(name:str) -> str:
	with open(name, "r", encoding=ENCODE) as f:
		return f.read()

def read_group(tokens:str) -> str:
	result     = ""
	command    = ""
	is_space   = -1
	is_linebk  = -1
	is_command = -1
	for token in tokens:
		yield token

for i in read_group(read_file(FILE)):
	print(i)
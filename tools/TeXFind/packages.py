import re
import sys


# Constant(s)
ENCODE = "utf-8"
FILE_P = "texlive-p"
with open(FILE_P, "r", encoding=ENCODE) as f:
	Dict = eval(f.read())

# Function(s)
def extract_preamble(string:str):
	pattern = "(?<=documentclass)[\s\S]+?(?=\\\\begin{document})"
	result  = re.findall(pattern, string)
	return result[0] if result else ""

def extract_packages(string:str):
	string  = re.sub("\s", "", string)
	pattern = "(?<=usepackage)[^}]+?}"
	group   = re.findall(pattern, string)
	pattern = "(?<={)[^}]+?(?=})"
	result  = []
	for i in range(len(group)):
		temp = re.findall(pattern, group[i])
		if temp:
			result += temp[0].split(",")
	return result

def findall_dependency(elems:set, result=set()):
	for e in elems:
		if e not in result:
			temp = Dict.get(e, [])
			if temp:
				result = result.union( temp )
				result = result.union( findall_dependency(temp, result) )
	return result.union( elems )


# Body(s)
if not sys.argv[1:]:
	raise FileNotFoundError()
with open(sys.argv[1], "r", encoding=ENCODE) as f:
	content = f.read()

packages = extract_packages(extract_preamble(content))

print(packages)

print(findall_dependency(packages))
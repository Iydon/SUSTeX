import re


def units():
	name = ["pt", "pc", "in", "bp", "cm", "mm", "dd", "cc", "sp"]
	conv = [1, 12, 72.27, 72*72.27, 2.54*72.27, 0.254*72.27, 1238/1157, 12*1238/1157, 1/65536]
	return dict(zip(name, conv))


def str2list(string):
	num = re.findall("[\d\.e]+", string)
	uni = re.findall("[a-z]+", string.lower())
	return [num[0], uni[-1]]


def process(lst, precise):
	dct = units()
	result = ["%s %s"%(lst[0], lst[-1])]
	pt = float(lst[0]) * float(dct[lst[-1]])
	for key in dct.keys():
		result.append("%%.%df %%s"%precise%(pt/float(dct[key]), key))
	return " = ".join(result)


def help():
	result = """
pt -> point (本手册的基线之间距离是12 pt)
pc -> pica (1 pc = 12 pt)
in -> inch (1 in = 72.27 pt)
bp -> big point (72 bp = 1 in)
cm -> centimeter (2:54 cm = 1 in)
mm -> millimeter (10mm = 1 cm)
dd -> didot point (1157 dd = 1238 pt)
cc -> cicero (1 cc = 12 dd)
sp -> scaled point (65536 sp = 1 pt)
	"""
	return result


precise = 4
while True:
	in_ = input(">> ")
	if not in_:
		break
	if "\\precise" in in_:
		precise = int(re.findall("\d+", in_)[0])
		continue
	if "help" in in_ or in_.lower()=="h":
		print(help())
		continue
	try:
		print(process(str2list(in_), precise))
	except:
		print("Bad input.")

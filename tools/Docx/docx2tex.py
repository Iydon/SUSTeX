import docx


document = docx.opendocx("demo.docx")

result = docx.getdocumenttext(document)

with open("demo.log", "a+", encoding="utf-8") as f:
	for r in result:
		f.write(r)
		f.write("\n")
		f.write("*"*ord("*"))
		f.write("\n")
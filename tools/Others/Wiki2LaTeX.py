import html
import re
import requests


def get_content_from_url(url:str):
    """
    https://en.wikipedia.org/wiki/Ambiguity_function
    https://en.wikipedia.org/w/index.php?title=Ambiguity_function&action=edit
    """
    # 转化链接
    url = url[url.rfind("/")+1:]
    url = "https://en.wikipedia.org/w/index.php?title=%s&action=edit"%url
    # 爬取内容
    response = requests.get(url)
    # 提取内容
    pattern  = "<textarea[\s\S]+</textarea>"
    content  =  re.findall(pattern, response.text)[0]
    content  = content[content.find(">")+1:content.rfind("<")]
    return html.unescape(content)



def parse_content(content:str):
    """
    Convert Wiki to LaTeX.
    """
    def add_preamble(content:str):
        r"""
        \documentclass, document environment.
        """
        preamble  = """\\documentclass{article}\n\\nonstopmode\n\\usepackage{amsmath,amssymb}\n"""
        preamble += """\\usepackage{graphicx}\n\\usepackage{hyperref}\n\\usepackage{xcolor}\n"""
        preamble += """\\begin{document}\n\\tableofcontents\\clearpage\n\n%s\n\\end{document}"""
        return preamble%content


    def convert_escape(content:str):
        r"""
        #, % and &
        """
        pattern = {"#": "\\#",
                   "%": "\\%",
                   "&": "\\&"}
        for p,v in pattern.items():
            content = content.replace(p, v)
        return content


    def convert_equation(content:str):
        r"""
        $...$ and \[...\]
        """
        pattern = {"(:<math>)([\s\S]+?)(</math>)": "\\[\n%s\n\\]",
                   "(<math>)([\s\S]+?)(</math>)":  "$%s$"}
        for p,v in pattern.items():
            f = lambda s: v%(s.groups()[1])
            content = re.sub(p, f, content)
        return content


    def convert_section(content:str):
        r"""
        \section, \subsection and \subsubsection.
        """
        pattern = {"(\n====)([\s\S]+?)(====\n)": "\n\\subsubsection{%s}\n",
                   "(\n===)([\s\S]+?)(===\n)":   "\n\\subsection{%s}\n",
                   "(\n==)([\s\S]+?)(==\n)":     "\n\\section{%s}\n",}
        for p,v in pattern.items():
            f = lambda s: v%(s.groups()[1])
            content = re.sub(p, f, content)
        return content


    def convert_href(content:str):
        """
        [[..]] and [...]
        """
        def f(s):
            g = s.groups()[1]
            url = lambda s: "https://en.wikipedia.org/wiki/%s"% \
                                s.replace(" ", "_")
            if g.count("|") == 0:
                return "\\href{%s}{%s}"%(url(g),g)
            elif g.count("|") == 1:
                g1,g2 = g.split("|")
                return "\\href{%s}{%s}"%(url(g1),g2)
            else:
                g1,g2 = g.split("|", maxsplit=1)
                g2 = "\\color{violet} File or Image"
                return "\\href{%s}{%s}"%(url(g1),g2)

        def g(s):
            f = s.groups()[1]
            return "\\url{%s}"%(f.replace(" ","_"))

        pattern = "(\[\[)([\s\S]+?)(\]\])"
        content = re.sub(pattern, f, content)
        pattern = "(\[)(http[\s\S]+?)(\])"
        content = re.sub(pattern, g, content)
        return content


    def convert_itemize(content:str):
        """
        *...
        """
        def f(s):
            g = "".join(s.groups())
            beginend = "\n\\begin{itemize}\n%s\n\\end{itemize}\n"
            s = re.sub("\n\*", "\n\\item", g)
            return beginend%s

        pattern = "((\n\*[^\n]+)+)"
        content = re.sub(pattern, f, content)
        return content


    def convert_ref(content:str):
        """
        <ref ... /> and <ref ... </ref>
        """
        bib = dict()
        idx = 0
        pattern = "<ref[\s\S]+?</ref>"
        for ref in re.findall("(<ref name=\")([^\"]+)(\"/>)", content):
            content = content.replace("".join(ref), "<ref name=\"%s\"></ref>"%ref[1])
        for ref in re.findall(pattern, content):
            if "<ref>" in ref:
                idx += 1
                name = str(idx)
            elif "name=\"" in ref:
                name = re.findall("(?<=ref name=\")([^\"]+)(?=\")", ref)[0]
            else:
                name = "Unknown"
            if name not in bib:
                bib[name] = ref[ref.find(">")+1:ref.rfind("<")]
            content   = content.replace(ref, "\\cite{%s}"%name, 1)
        bibiliography = """\\\\begin{thebibliography}{%s}\n%s\n\\\\end{thebibliography}"""
        reflist = bibiliography%("9"*len(str(len(bib))), \
                      "\n".join(["\\\\bibitem{%s} %s"%(k,v) for k,v in bib.items()]))
        content = re.sub("{{reflist[\s\S]+?}}", reflist, content)
        return content


    tr = convert_escape(content)
    tr = convert_equation(tr)
    tr = convert_section(tr)
    tr = convert_href(tr)
    tr = convert_itemize(tr)
    tr = add_preamble(tr)
    tr = convert_ref(tr)
    return tr




print("Please enter the Wikipedia url:")
url = input(">>> ")
content = get_content_from_url(url)
result  = parse_content(content)

with open("result.tex", "w", encoding="utf-8") as f:
	f.write(result)

import re


def convert(txt):
    txt = image(txt)
    txt = code(txt)
    txt = header(txt)
    txt = numbered_list(txt)
    txt = normal_list(txt)
    txt = pukiwiki_plugin(txt)
    txt = table_attr(txt)
    txt = lsx(txt)
    txt = link(txt)
    txt = hash(txt)
    txt = misc(txt)
    txt = table(txt)
    return txt


def header(txt):
    txt = re.sub(r"^\*\*\*\*\*", "##### ", txt, flags=re.MULTILINE)
    txt = re.sub(r"^\*\*\*\*", "#### ", txt, flags=re.MULTILINE)
    txt = re.sub(r"^\*\*\*", "### ", txt, flags=re.MULTILINE)
    txt = re.sub(r"^\*\*", "## ", txt, flags=re.MULTILINE)
    txt = re.sub(r"^\*", "# ", txt, flags=re.MULTILINE)
    return txt


def lsx(txt):
    txt = re.sub("#lsx", "$lsx", txt, flags=re.MULTILINE)
    txt = re.sub("sort=date", "sort=updatedAt", txt, flags=re.MULTILINE)
    txt = re.sub("except=.*,", "", txt, flags=re.MULTILINE)
    txt = re.sub(",info", "", txt, flags=re.MULTILINE)
    txt = re.sub("num=:", "num=", txt, flags=re.MULTILINE)
    txt = re.sub(",reverse=on", "reverse=true",txt,flags=re.MULTILINE)
    txt = re.sub(",reverse=off", "",txt,flags=re.MULTILINE)
    txt = re.sub(",reverse=false", "",txt,flags=re.MULTILINE)
    return txt


def link(txt):
    txt = re.sub(r"\[\[([^:]*):([^\]]*)]]",
                 "[\\1](\\2)\n", txt, flags=re.MULTILINE)
    return txt


def misc(txt):
    txt = re.sub("&yen", "¥", txt, flags=re.MULTILINE)
    txt = re.sub(r"&font\(.*\){(.*)};", "\\1", txt)
    txt = re.sub(r"&size\(.*\){(.*)};", "\\1", txt)
    txt = re.sub(r"&color\(.*\){(.*)};", "\\1", txt)
    txt = re.sub(r"&ruby\(.*\){(.*)};", "\\1", txt)
    # codeblock, region, endregion, etc...
    txt = re.sub("^}}", '\n', txt, flags=re.MULTILINE)
    # newline
    txt = re.sub("&br|#br;", "\n", txt, flags=re.MULTILINE)
    # 打ち消し
    txt = re.sub("%%", "~~", txt, flags=re.MULTILINE) 
    return txt

def hash(txt):
    txt = re.sub(r"(?<!\S)#\S+", "", txt,  flags=re.MULTILINE)
    txt = re.sub(r"\[#[0-9a-z]+\]", "", txt, flags=re.MULTILINE)
    return txt


def table_attr(txt):
    txt = re.sub(
        r"(TLEFT|tleft|LEFT|left|RIGHT|right|tright|TRIGHT|CENTER|center|TCENTER|tcenter):", "", txt)
    txt = re.sub(r"(BGCOLOR|COLOR|SIZE)\(.[^:]*\):", "", txt)
    txt = re.sub(r"(FC|CC):#[A-Fa-f0-9]{6} ?", '', txt, flags=re.MULTILINE)
    return txt


def normal_list(txt):
    txt = re.sub("^---", "- ", txt, flags=re.MULTILINE)
    txt = re.sub("^--", "- ", txt, flags=re.MULTILINE)
    txt = re.sub("^-([^ ])", "- \\1", txt, flags=re.MULTILINE)
    return txt


def pukiwiki_plugin(txt):
    txt = re.sub(
        r"#(navi|freeze|contents|ls2|norelated|nofollow|hr|p?comment|article|vote|amazon|bugtrack|calendar)", '', txt, flags=re.MULTILINE)
    txt = re.sub(r"#(block|pginfo|region|endregion).*",
                 '', txt, flags=re.MULTILINE)
    return txt


def code(txt):
    txt = re.sub(r"#code\((.*?)\)\{\{", r"```\1\n", txt, flags=re.MULTILINE)
    return txt


def image(txt):
    txt = re.sub(
        r'&ref\(((.*\.(jpg|jpeg|png|gif|PNG|JPEG|JPG|GIF))).*', r'\n$refimg(\1)\n', txt, flags=re.MULTILINE)
    txt = re.sub(r"\.(PNG|png|JPG|JPEG|jpeg|jpg)",
                 ".webp", txt, flags=re.MULTILINE)
    return txt


def numbered_list(txt):
    txt = re.sub(r"^\+\+\+", "  1. ", txt, flags=re.MULTILINE)
    txt = re.sub(r"^\+\+", " 1. ", txt, flags=re.MULTILINE)
    txt = re.sub(r"^\+", "1. ", txt, flags=re.MULTILINE)
    return txt


def table(txt):
    table_head_pattern0 = r'^\|[^c]*\n\|*.\|c'
    table_head_pattern1 = r'^\|.*c\n\|~.*'
    table_head_pattern2 = r'^\|~.*\n\|[^-\n]*'
    table_head_pattern3 = r'^\|.*c\n\|[^-\n]*'

    p0 = re.search(table_head_pattern0, txt, re.MULTILINE)
    p1 = re.search(table_head_pattern1, txt, re.MULTILINE)
    p2 = re.search(table_head_pattern2, txt, re.MULTILINE)
    p3 = re.search(table_head_pattern3, txt, re.MULTILINE)
    while re.search(table_head_pattern0, txt, re.MULTILINE):
        matcher = re.search(table_head_pattern0, txt, re.MULTILINE)
        header = matcher.group().split('\n')[0]
        table_separator = re.sub(r'\|', '|-',  matcher.group().split('\n')[1])
        # remove last character c
        table_separator = table_separator[:-1]
        txt = '\n' + '\n' + txt[:matcher.start()] + header + '\n' + \
            table_separator + txt[matcher.end():]
    while re.search(table_head_pattern1, txt, re.MULTILINE):
        matcher = re.search(table_head_pattern1, txt, re.MULTILINE)
        header = matcher.group().split('c\n')[1]
        header = re.sub(r'~', '', header)
        table_separator = re.sub(r'\|[^\|]+', '|-', header)
        txt = '\n' + '\n' + txt[:matcher.start()] + header + '\n' + \
            table_separator + txt[matcher.end():]
    while re.search(table_head_pattern2, txt, re.MULTILINE):
        matcher = re.search(table_head_pattern2, txt, re.MULTILINE)
        header = matcher.group().split('\n')[0]
        firstRow = matcher.group().split('\n')[1]
        table_separator = re.sub(r'\|\~.*?(?=\||$)', '|-', header)
        header = re.sub(r'~', '', header)
        txt = '\n' + '\n' + txt[:matcher.start()] + header + '\n' + \
            table_separator + '\n' + firstRow + txt[matcher.end():]
    while re.search(table_head_pattern3, txt, re.MULTILINE):
        matcher = re.search(table_head_pattern3, txt, re.MULTILINE)
        head = matcher.group().split('\n')[0]
        firstRow = matcher.group().split('\n')[1]
        emptyHeader = re.sub(r'[^\|]', '', head)
        table_separator = re.sub(r'\|[^\|]*', '|-', head)
        txt = '\n' + '\n' + txt[:matcher.start()] + emptyHeader + '\n' + table_separator + '\n' +\
            firstRow + txt[matcher.end():]
    return txt

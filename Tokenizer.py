import nltk
from bs4 import BeautifulSoup
import os
import sys
import string

punct = ['!',"''","'", '#', '"','``', '%', '$', '&', ')','”','“','.','(', '+', '*', '-','[',']','{','}',':',';',"b'",'"','"',',']

def letsdoit(url,xx):
    global rt
    global st
    os.chdir(rt)


    html = open(url, 'r', encoding='utf-8')

    soup = BeautifulSoup(html,"html.parser")
    print("hi")
    url=url.split(".html")
    til=url[0]+".txt"



    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())

    parts = (phrase.strip() for line in lines for phrase in line.split("  "))

    text = '\n'.join(pt for pt in parts if pt)
    text=text.replace('\\n', '\n').replace('\\t', '\t')
    x=xx
    print("ih")
    if (x == "1"):
        text=text.lower()
        tokens = nltk.word_tokenize(text)
    if (x == "2"):
        tokens= []
        see = nltk.word_tokenize(text)
        for i in see :
            if i not in string.punctuation and i not in punct and "\\x" not in i and not i.startswith(('+\\', '+','*')):

                try:
                    i.encode(encoding='utf-8').decode('ascii')
                except UnicodeDecodeError:
                    print("wrong")
                else:
                    tokens.append(i)
                    #C: / Users / Rahul / Desktop / IRproject
    if(x == "3"):
        text = text.lower()
        token = nltk.word_tokenize(text)
        tokens = []

        for i in token:
            if i not in string.punctuation and i not in punct and "\\x" not in i and not i.startswith(('+\\','www','doi','//','/','*')):

                try:

                    i.encode(encoding='utf-8').decode('ascii')
                except UnicodeDecodeError:
                    print("non - english word")
                else:
                    if "-" in i:
                        i=i.split("-")
                        tokens.append(i[0])
                        tokens.append(i[1])
                    else:
                        tokens.append(i)
            if i in ("pm","am"):
                break
    else:
        x="4"

    os.chdir(st)
    if (x != "4"):
        print("done")
        # f = open(til, 'w', encoding='utf-8')
        # for i in tokens:
        #     f.write(str(i) + " ")
        # f.close




# rt = input("Enter the dir folder where the downlaoded rawtext is stored : "
#            "please use / frontslash when typing in directory path: ")
rt= os.path.join(sys.path[0], "cacm")
# st = input("Enter the dir folder where u want to store the doc with space : "
#            "please use / frontslash when typing in directory path: ")
st=os.path.join(sys.path[0], "SP")
os.chdir(rt)
y=os.listdir(os.curdir)
x=input("enter your choice"
        "1. for case folding "
        "2. for punctuation  "
        "3. for both case folding and punctuation ")
for i in y:
    print(i)

    letsdoit(i, x)

    # print(tokens)
#C:\\Users\\Rahul\\PycharmProjects\\rawtext\\rawtextdown
#C:\\Users\\Rahul\\PycharmProjects\\rawtext\\SP
#
# C:\\Users\\Rahul\\Desktop\\IR project
# C:\\Users\\Rahul\\Desktop\\SP
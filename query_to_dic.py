import os
import sys
qid_query = {}
m=0
fh = open("cacm_query.txt", 'r', encoding='utf-8')
str1=" "
for line in fh:

    if line.startswith("<DOC>"):
        m=m+1

    elif line.startswith("<DOCNO>"):

        str1=""
    elif line.startswith("\n"):

        str1=str1
    elif line.startswith("</DOC>"):

        qid_query[m] = str1.lstrip().rstrip()
    else:

        line=line.rstrip()
        str1 = str1 + " " +line


# file = open("querytofire.txt", 'w', encoding='utf-8')
# for i in qid_query:
#     file.write(str(i)+" " +qid_query[i]+"\n")
# file.close()



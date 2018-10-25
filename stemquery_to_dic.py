import os
import sys
stemqid_query = {}
m=0
fh = open("cacm_stemquery.txt.txt", 'r', encoding='utf-8')

for line in fh:
    line=line.split(">>")
    stemqid_query[line[0]]=line[1]

# for i in stemqid_query:
#     print(stemqid_query[i])

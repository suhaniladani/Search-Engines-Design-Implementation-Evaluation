import os
import sys
stopwordlist = []
fh = open("common_words.txt", 'r', encoding='utf-8')
for line in fh:
    line=line.split("\n")

    stopwordlist.append(line[0])
fh.close()



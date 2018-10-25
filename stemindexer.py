import os
import sys
import string
fh = open("waste", 'w', encoding='utf-8')
with open("cacm-stem.txt", encoding='utf-8') as f:
    for line in f:
        if line.startswith("#"):
            line=line.split(" ")
            fh.close()
            if len(line[1].rstrip())==1:
                til="000"+line[1]
            if len(line[1].rstrip())==2:
                til="00"+line[1]
            if len(line[1].rstrip())==3:
                til="0"+line[1]
            if len(line[1].rstrip())==4:
                til=line[1]
            os.chdir("C:\\Users\\Rahul\\PycharmProjects\\IRpr\\Stem-SP")
            fh = open("CACM-"+til.rstrip()+".txt", 'w', encoding='utf-8')

        else:
            fh.write(line)





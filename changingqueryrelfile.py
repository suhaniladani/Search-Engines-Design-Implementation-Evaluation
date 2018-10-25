import os
import sys
stopwordlist = []
fh = open("queryrel.txt", 'r', encoding='utf-8')
for line in fh:
    line=line.split(" ")
    chag=line[2]
    chag=chag.split("-")
    if len(chag[1].rstrip()) == 1:
        til = "000" + chag[1]
    if len(chag[1].rstrip()) == 2:
        til = "00" + chag[1]
    if len(chag[1].rstrip()) == 3:
        til = "0" + chag[1]
    if len(chag[1].rstrip()) == 4:
        til = chag[1]
    chag[1]=til
    #print(line[0]+" " + line[1]+" " + chag[0] + "-"+ chag[1]+" "+ line[3].rstrip())


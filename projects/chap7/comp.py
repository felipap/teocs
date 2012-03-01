#!/usr/bin/env python3

import sys

if len(sys.argv) < 3:
    print("not valid. usage: comp.py <file1> <file2>")
    sys.exit(1)

file1 = open(sys.argv[1],'r')
file2 = open(sys.argv[2],'r')

lines1 = file1.readlines()
lines2 = file2.readlines()

if len(lines1) < len(lines2):
    lines1, lines2 = lines2, lines1
    file1, file2 = file2, file1

print("files:\n",file1.name,'\t\t',file2.name)
for i in range(len(lines1)):
    l1 = lines1[i].replace('\n','')
    l2 = lines2[i].replace('\n','')
    print(str(i)+':',l1,'\t\t',l2,'DONT MATCH' if l1!=l2 else '')

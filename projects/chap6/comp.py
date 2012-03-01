#!/usr/bin/env python3
""" a """

import sys

def main():
    """ does the crappy stuff """
    
    file1 = open(sys.argv[1],'r')
    file2 = open(sys.argv[2],'r')
    content1 = file1.readlines()
    content2 = file2.readlines()

    if len(content1) < len(content2):
        content1, content2 = content2, content1
        file1, file2 = file2, file1

    print("files:\n", file1.name, '\t\t', file2.name)
    for i in range(len(content1)):
        line1 = content1[i].replace('\n', '')
        line2 = content2[i].replace('\n', '')
        print(str(i)+':', line1, '\t\t', line2, 'DONT\
                 MATCH' if line1!=line2 else '')

if __name__ == '__main__':

    if len(sys.argv) < 3:
        print("not valid. usage: comp.py <file1> <file2>")
        sys.exit(1)

    main()

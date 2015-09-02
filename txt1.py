#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 31 23:32:33 2015

@author: ja
"""

import sys

dato=open('zadatak1.txt', 'r')
log=open('jedan.log', 'a')
lin=dato.readline()
print("prva {}.\n").format(lin[:-1])
log.write(lin)
dato.close()
log.close()

l1=[0, 9]
print("l1: {0}".format(l1))
l2=[l1]
print("l2=l1:\n  l2: {0}".format(l2))
l3=[l1[:]]
print("l3=l1[:]:\n  l3: {0}".format(l3))
l2.append([4, 5])
l3.append([4, 5])
print("l2.append, l3.append:\n  l2: {0};\n  l3: {1}".format(l2, l3))
l1.pop(0)
print("l1.pop(0):\n  l1: {0};\n  l2: {1};\n  l3: {2}".format(l1, l2, l3))

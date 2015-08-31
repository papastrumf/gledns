#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 23 2015

@author: ja

trt mrt
"""

import sys
import re


def main():
    snli=('iso.3.6.1.4.1.10704.1.1.1.1.6.83.49.95.114.116.114 = STRING: "S1_rtr"', 'iso.3.6.1.4.1.10704.1.1.1.1.6.83.49.95.118.112.110 = STRING: "S1_vpn"')
    pfx="iso.3.6.1.4.1.10704"
    for s1 in snli:
        m1=re.search(r'\d{2,9}.(?P<jen>[\d+\.]+) =.+: "(?P<dva>\w+)"', s1)
#        print(str(m1.groupdict()))
        oid=m1.group('jen')
        ime=m1.group('dva')
        print("A: %s - B: %s." % (oid, ime))


if __name__ == '__main__':
    main()


#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 12:53:43 2015

@author: ja
"""


import re

def main():
    with open('useri.txt', 'r') as dato:
        line = dato.readlines()
    for li1 in line:
#        m1=re.search(r'(?P<jen>[\w]+)\t(?P<dva>[\S]+)\t(?P<tri>[\w]+))', li1)
        m1=re.search(r'(?P<jen>\w+)\t(?P<dva>[\w\ \x87\x8d\xa1\xbe\x91\xa0]+)\t(?P<tri>[\w-]+)', li1, re.UNICODE)
#        print(str(m1.groupdict()))
        user=m1.group('jen')
        ime=m1.group('dva')
        grupa=m1.group('tri')
#        print("user %s\n comment \"%s\"\n vpn-client-access group \"VPN mreze 1\"\n member-of \"%s\"\n exit\n" % (user, ime, grupa))
        print("user %s" % user)
        print(" password temPa$124\n comment \"IN2: %s\"" % ime)
        print(" vpn-client-access group \"VPN mreze 1\"")
        print(" member-of \"%s\"\n member-of \"VPN_grupa\"\n exit\n" % grupa)
    dato.close()


if __name__ == '__main__':
    main()


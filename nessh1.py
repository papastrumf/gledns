#!/usr/bin/python

"""
  citaj /var/log/auth.log i azururaj iptables

  ver 0.9.4
  05.03.2015
"""

import sys
import re
import subprocess
import os

AUTHLOG="/var/log/auth.log"
DAT="/usr/local/etc/nessh1.dat"
LOG="/var/log/nessh1.log"
DODAJ=0
MAKNI=1
FWRplus=['/sbin/iptables', '-I', 'INPUT', '1', '-s', '1.1.1.1', '-j', 'DROP']
FWRminus=['/sbin/iptables', '-D', 'INPUT', '-s', '1.1.1.1', '-j', 'DROP']
GRAN1=5		# granica dodavanja u zabranu
GRAN2=25	# granica ispod koje se brojac uvecava, da bi zabrana trajala bar 1 sat
MNDOD=7		# broj za koji se uvecava brojac kad je manji od GRAN2
ARLIN=2500	# max broj linija procitanih iz log-a u jednom prolazu
VER="0.9.4"

alptr=0 	# auth.log trenutna pozicija
srip=[] 	# popis source IP-a
asip=[] 	# popis src IP za koje treba uvesti zabranu
rsip=[] 	# popis src IP za koje treba maknuti zabranu
ncna=0		# broj novih pokusaja (u zadnjem intervalu)


"""
	ucitaj podatke iz .dat file-a, koji drzi trenutnu poziciju (do kuda je procitano)
	auth.log datoteke (ALOP) i listu source IP adresa (SIPA) sa brojem pokusaja i
	stanjem zabrane (+ / -)
"""
def citajDat():
	global alptr, dat, srip

	for red in dat :
		r1=re.search(r'ALOP=(?P<br>\d+)', red)
		if r1 :
			alptr=int(r1.group('br'))
			
		r2=re.search(r'SIPA=(?P<ip>[\d+\.]+):(?P<nm>\d+):(?P<st>[\+-])', red)
		if r2 :
			srip.append([r2.group('ip'), int(r2.group('nm')), r2.group('st')])

	#print("br: %d, du: %d" % (alptr, len(srip)))
		

"""	
	ucitaj dodatnih 2500 linija iz auth.log datoteke, iz linija gdje je dojavljen
	neuspjeli pokusaj spajanja (SSH protokolom) uzima se source IP adresa i dodaje
	u popis; ako je broj pojavljivanja veci od 5 dodaje se u popis za dodavanje 
	zabrane
"""
def citajAuthLog():
	global alptr, fal, srip, asip, ncna

	if os.path.getsize(AUTHLOG) >= alptr:
		fal.seek(alptr)

	redbr=0
	for red in fal :
		r1=re.search(r'.*sshd\[\d+\]: Failed password for invalid user (?P<usr>\w+) from (?P<ipa>([\d+\.])+).*', red)
		if r1 :
			ipa=r1.group('ipa')
			usr=r1.group('usr')
			#print("ip: %s; usr: %s" % (ipa, usr))
			ima1=0
			ima2=0
			br=0
			ncna += 1
			for (ip1, nm1, st1) in srip :
				if ip1 == ipa :
					ima1=1
					if nm1 >= GRAN1 -1 and st1 is "-" :
						#print("+ip,nm: %s" % srip[br])
						for ip2 in asip :
							if ip2 == ip1 :
								ima2=1
						
						if ima2 == 0 :
							asip.append(ip1)
					
					srip[br] = [ip1, nm1+1, st1]
					#print("ip,nm: %s" % srip[br])
				br += 1
			
			if ima1 == 0 :
				srip.append([ipa, 1, "-"])
		
		redbr += 1
		if redbr > ARLIN :
			break
	
	alptr=fal.tell()
	

"""
	azuriranje IPtables ruleova
"""
def modFWr(op, srcIP):
	if op == DODAJ:
		FWRplus[5] = srcIP
		nardb = FWRplus
	elif op == MAKNI:
		FWRminus[4] = srcIP
		nardb = FWRminus
	
#	print(nardb)
	subprocess.call(nardb)


"""
	zapisivanje trenutnog stanja i promjena u log datoteku
"""
def Logiraj():
	global asip, rsip, alptr, srip

	try:
		log=open(LOG, 'a')
	except:
		print("Dato",LOG,"nedostupna!")
		sys.exit(4)
	
	##danvri=subprocess.check_output(['date', '"+%d.%m.%y %H:%M"'], shell=True)
	danvri=subprocess.check_output(['date "+%d.%m.%y %H:%M"'], shell=True)
	log.write("-----\n%s" % danvri);
	if len(asip) > 0:
		log.write("FWplus: %s\n" % asip)
	if len(rsip) > 0:
		log.write("FWminus: %s\n" % rsip)
	# privr. - sve adrese:
	log.write("%")
	brmi=0
	for (ip1, nm1, st1) in srip :
		st2=""
		if st1 is "-" :
			st2=st1
			brmi += 1
		log.write(" %s=%d%s;" % ( ip1, nm1, st2))
	log.write(" %\n")
	if brmi > 0 :
		sipmi="-"
	else :
		sipmi=""
	log.write("alop: %d, nsip: %d%s, ncna: %d\n" % (alptr, len(srip) - len(rsip), sipmi, ncna))
	log.close()


"""
	glavna procedura
"""
def main():
	global fal, dat, srip

	try:
		fal=open(AUTHLOG, 'r')
	except:
		print("Dato",AUTHLOG,"nedostupna!")
		sys.exit(2)
	
	try:
		dat=open(DAT, 'r+')
	except:
		print("Dato",DAT,"nedostupna!")
		if fal :
			fal.close()
		sys.exit(2)

	citajDat()
	citajAuthLog()

	dat.seek(0)
	dat.write("ALOP=%d\n" % alptr)
	br=0
	for (ip1, nm1, st1) in srip :
		if nm1 > 0 :
			if nm1 >= GRAN1 :
				if st1 is "-" :
					st1 = "+"
					if nm1 < GRAN2 :
						nm1 += MNDOD
				
				srip[br] = [ip1, nm1, st1]
			
			dat.write("SIPA=%s:%d:%s\n" % (ip1, nm1-1, st1))
		elif st1 is "+" :
			rsip.append(ip1)
			modFWr(MAKNI, ip1)

		br += 1
	
	for ip1 in asip :
		modFWr(DODAJ, ip1)

	dat.write("%s\n" % VER)
	fal.close()
	datptr=dat.tell()
	dat.truncate(datptr)
	dat.close()

	Logiraj()

"""
	kraj main procedure
"""

if __name__ == '__main__':
    main()


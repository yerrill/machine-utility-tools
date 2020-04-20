import requests
import sys
import datetime
import json

domain = None
u = None
p = None

lastIP = None
newIP = None

confFile = str(sys.argv[1])
#logFile = str(sys.argv[2])

def log(st):
	print(f"{datetime.datetime.now()}\t{domain}\t{st}")
	#s = open(logFile, mode='a')
	#s.write(f"{datetime.datetime.now()}\t{domain}\t{st}\n")
	#s.close()

def loadConf():
	global domain, u, p, lastIP
	st = None
	try:
		s = open(confFile, mode='r')
		st = s.read()
		s.close()
	except:
		log("Conf File Load Error")
	
	try:
		d = json.loads(st)
		domain = d["domain"]
		u = d["username"]
		p = d["password"]
		lastIP = d["last"]
	except:
		log(f"JSON load error\n{st}")

def outConf(ip):
	global domain, u, p, lastIP
	d = {"domain": domain, "username": u, "password": p, "last": ip}
	jsond = json.dumps(d)
	try:
		s = open(confFile, mode='w')
		s.write(jsond)
		s.close()
	except:
		log("Conf File Output Error")

def checkIP():
	global newIP
	ip = requests.get("https://domains.google.com/checkip")
	ip = ip.text
	if ip != lastIP:
		newIP = ip

def update():
	if u and p and domain:
		rq = f"https://{u}:{p}@domains.google.com/nic/update?hostname={domain}"
		s = requests.get(rq)
		log(s.text)
	else:
		log("Values Missing")

loadConf()
checkIP()
if newIP != None:
	update()
	outConf(newIP)
	log(f"{lastIP} -> {newIP}")
else:
	log(f"No Change: {lastIP}")

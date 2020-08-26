#!/usr/bin/env python
import socket
import os
import argparse
import subprocess
openp = []
parser = argparse.ArgumentParser(description="The ImLazy By Ofir Dassa:")
parser.add_argument("-tP","--topports", action='store_true', help="Scan the top 20 common ports")
parser.add_argument("-p","--ports",type=str, help="range of ports. EX: -p=1-445")
parser.add_argument("-ip", type=str, required=True)
args = parser.parse_args()
def Ping():
        	response = os.system("ping -c 1 " + args.ip)
		if response == 0:
			return True
		else:
			print ("Ureachable host")
			return False
def PortScan():
	if args.topports:
		print("scanning fot 20 top ports")
		ports = [21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080]
		for i in ports:
			try:
				s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
				s.settimeout(5)
				s.connect((args.ip,i))
				print str(i) + " is open!"
				openp.append(i)
				s.close()
		
			except KeyboardInterrupt:
				exit()
			except:
				pass
	elif args.ports.find('-')!=-1:
		port=args.ports.split('-')
		for i in range(int(port[0]),int(port[1])+1):
			try:
				s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
				s.settimeout(5)
				s.connect((args.ip,i))
				print str(i) + " is open!"
				openp.append(i)
				s.close()
			
			except KeyboardInterrupt:
				exit()
			except:
				pass
	elif args.ports.find(',')!=-1:
		ports=args.ports.split(',')
		for i in ports:
			try:
				s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
				s.settimeout(5)
				s.connect((args.ip,int(i)))
				print str(i) + " is open!"
				openp.append(int(i))
				s.close()
			
			except KeyboardInterrupt:
				exit()
			except:
				pass
	else:
		for i in range(1,65536):
			try:
				s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
				s.settimeout(5)
				s.connect((args.ip,i))
				print str(i) + " is open!"
				openp.append(i)
				s.close()
			
			except KeyboardInterrupt:
				exit()
			except:
				pass
def ftpcheck(ip):
	import ftplib
	try:
		ftp=ftplib.FTP(ip)
		ftp.login()
		print("[+] Anonymous login is available with the FTP server!")
		ftp.quit()
		return True
	except:
		return False

def grab_banner(ip_address,port):  
      try:  
           s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)  
           s.connect((ip_address,port))  
           banner = s.recv(1024)  
           return banner.decode() 
      except:  
           return

def osDetection(ip):
	ping = subprocess.Popen("ping -c 1 "+ip+" | grep -i 'ttl' | awk '{print $6}' | sed 's/.*=//'" , shell=True, stdout=subprocess.PIPE)
	ttl=ping.communicate()[0]
	if int(ttl)==64:
		print("[+] OS Detection! ----- Probably Unix/Linux, Google's customized Linux or FreeBSD")
	elif int(ttl)==128:
		print("[+] OS Detection! ----- Probably Windows XP, 7, Vista or Server 2008")
	elif int(ttl)==254:
		print("[+] OS Detection! ----- Probably Solaris/AIX")
	elif int(ttl)==255:
		print("[+] OS Detection! ----- Probably Cisco Router ")
	else:
		return
if __name__ == "__main__":
	if Ping():
		osDetection(args.ip)
		PortScan()
		i=0
		while i<=len(openp):
			port=openp[i]
			if ((port !=str(80)) or (openp[i] !=str(443))):
				banner = grab_banner(args.ip,port)	
				if banner and (not banner.isspace()):
					print("[+] Port "+str(port)+" with the banner of ----- "+str(banner))
			if port==21:
				ftpcheck(args.ip)
			if port==80 or port==443:
				import requests as req
				from lxml.html import fromstring
				print("[+] Host Web Page Title Is: " + fromstring(req.get("http://"+args.ip).content).findtext('.//title'))
			i=i+1
			banner = ""

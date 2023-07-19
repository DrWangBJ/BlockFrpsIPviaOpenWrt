#!/usr/bin/python
# encoding:utf-8
import ipaddress
import os
import time
def getIP():
	with open("/root/firewall.user","r") as f:
		lines=f.readlines()
		lines=lines[20:]
	#print(lines)
	IP=[]
	SUB=[]
	for line in lines:
		ip=line.split()[-1].strip()
		if "/" not in ip:
			IP.append(ip)

		sub=ip.split(".")[0:3]
		subnet=sub[0]+"."+sub[1]+"."+sub[2]+"."+"0/24"
		SUB.append(subnet)
		SUB=list(sorted(set(SUB)))
	#print(SUB)
	#print(IP)
	return IP,SUB

def CountIPs(IP,SUB):
	ipsub=[]
	ips=[ipaddress.ip_address(unicode(x)) for x in IP]
	for sub in SUB:
		subnet=ipaddress.ip_network(unicode(sub))
		count=0
		getip=" "
		#print(sub)
		for ip in ips:
			#ipt=ipaddress.ip_address(unicode(ip))
			if ip in subnet:
				getip=str(ip)
				count+=1
		if count==0 or count>1:
			#print(getip)
			ipsub.append(sub)
		else:
			ipsub.append(getip)
	return(ipsub)
	#print(ipsub)

# 创建一个掩码为24的网段对象
#subnet = ipaddress.ip_network(unicode("192.168.1.0/24"))

# 创建一个IP地址对象
#ip = ipaddress.ip_address(unicode("192.168.1.100"))

# 判断IP地址是否在网段内
#if ip in subnet:
#    print("is in ")
#    RE=getIP()
#    print(CountIPs(RE[0],RE[1]))
#else:
#    print("is not in ")
def repfile():
	os.system("cp /root/firewall.userbak /root/firewall.u")

def repfire():
	# os.system("cp /etc/firewall.user /root/log/firewall.user")
	os.system("cp /root/firewall.u /etc/firewall.user")

def add2ipset2(ip):
	#print(ip)
	tt=time.localtime(time.time())
	with open("/root/log/block.log","a") as logfile:
		logfile.write("operation at {}-{}-{}-{}-{}\n".format(tt.tm_year,tt.tm_mon,tt.tm_mday,tt.tm_hour,tt.tm_min))
		for i in ip:
			logfile.write("{} added to ipsets : {}-{}-{}\n".format(i,tt.tm_year,tt.tm_mon,tt.tm_mday))
	with open("/root/firewall.u","a") as f:
		for i in ip:
			f.write("ipset -exist add myipset {}\n".format(i))

repfile()
RE=getIP()
add2ipset2(CountIPs(RE[0],RE[1]))
repfire()
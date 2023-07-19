#!/usr/bin/python
#coding:utf-8
import ipaddress
import time
from insub import *
def check(ip,subnet):
	ip=ipaddress.ip_address(unicode(ip))
	subnet=ipaddress.ip_network(unicode(subnet))
	#test1=ip in subnet
	#test2=ip
	#print("{},{}".format(ip,subnet))
	return ip in subnet

def add2ipset(ip):
	print(ip)
	tt=time.localtime(time.time())
	with open("/root/log/block.log","a") as logfile:
		for i in ip:
			logfile.write("{} added to ipsets : {}-{}-{}\n".format(i,tt.tm_year,tt.tm_mon,tt.tm_mday))
	with open("firewall.user","a") as f:
		for i in ip:
			f.write("ipset -exist add myipset {}\n".format(i))

def checkwhitelist(lines,ipstr):
	#print(ipstr)
	for line in lines:
		content=line.split(" ")
		#print(content)
		if all(x.strip() in ipstr for x in content):
			#print("white")
			return True
			#break
	return False

def checkip(filename):
	new_ipset=[]
	flag=0
	with open(filename,"r") as text_file:
		ips=[line.split(",",1)[0] for line in text_file]
		#ipstrs=text_file.readlines()
	#print(ips)
	with open("firewall.user","r") as a_file:
		subsets=[line.split(" ")[-1].strip() for line in a_file]
	#print(subsets[20:22])
	subsetss=subsets[20:]
	#print(subsetss)
	for ip in ips:
		for subset in subsetss:
			re=check(ip,subset)
			#print(re)
			if re:
				flag=0
				break#print("have")
				#return True
			else:
				#add2ipset(ip)
				flag=1
		#print(flag)
		if flag:
			new_ipset.append(ip)

	#print(new_ipset)
	add2ipset(new_ipset)
#		lines=text_file.readlines()
#		for line in lines:
#			ip=line.split(",",1)[0]

	

def checkip2(filename):
	flag=0
	new_ipset=[]
#define a list to store ips need to be block
	with open("whitelist.txt","r") as file:
		lines=file.readlines()
#read whitelist lines

	with open(filename,"r") as text_file:
		ipstrs=text_file.readlines()
	#print(ipstrs)
#read target ips

	with open("firewall.user","r") as a_file:
		subsets=[line.split(" ")[-1].strip() for line in a_file]
#read ipset subsets from firewall.user

	#print(subsets[20:22])
	subsetss=subsets[20:]
#extract ipset subsets
	#print(subsetss)
	for ipstr in ipstrs:#for each target ips
		#print(ipstr)
		if checkwhitelist(lines,ipstr.strip()):#check is this ipstr is defined in whitelist line
			#white
			print("{} white".format(ipstr.strip()))
		else:
			print("{} block".format(ipstr.strip()))
			ip=ipstr.split(",")[0] #extract ip from ipstr
			#print(ip)
			for subset in subsetss: #for each subsets
				re=check(ip,subset) #check is this ip in subset
				if re: 
					flag=0
					break
					#print("have")
					#return True
				else:
					flag=1
					#add2ipset(ip)

			if flag:
				new_ipset.append(ip) #not contained, append it to the list

	add2ipset(new_ipset)

checkip("ip-check.txt")
checkip2("ip-check-cn.txt")
repfile() #copy a file named firewall.u from a bakupfile of firewall.user named firewall.userbak to local path, in which contains other rules
RE=getIP() #read IP and subnet from firewall.user
add2ipset2(CountIPs(RE[0],RE[1])) #add rules to firewall.u in local path
repfire()# replace the copyed file to /etc/firewall.user

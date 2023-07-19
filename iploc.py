#!/usr/bin/python
#coding:utf-8
 
import os
import subprocess
import time
#https://ip.cn/ip/134.122.94.225.html
URL = 'https://ip.cn/ip/'
 
def checkIP(ip):
    Headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.56"}
    try:
        Url=URL+ip+".html"
        print(Url)
        response = requests.get(url=Url,headers=Headers,timeout=20)
        #response = requests.get(url=Url,timeout=2)
        html=response.text
        stId1=html.find("address")
        addr=html[stId1+9:stId1+30]
        stId2=addr.find("<")
        addr=addr[0:stId2]
        #print(stId1)
        #print(addr)
        result=ip + "," + addr
        return result
    except:
        return "%s: timeout" % ip

def subprocess_popen(statement):
    p = subprocess.Popen(statement, shell=True, stdout=subprocess.PIPE)
    result=[]
    while p.poll() is None:
	#result=[]
        if p.wait() is not 0:
            print("error, check")
            result.append('e')
            return result
        else:
            re = p.stdout.readlines()
            #result = []
            for i in range(len(re)):
                res = re[i].decode('utf-8').strip('\r\n')
                result.append(res)
            return result
    #return result

def checkIP2(ip):
	try:
		cmd='curl --connect-timeout 5 --max-time 8 -s "https://ip.cn/ip/'+ip+'.html"'
		print(cmd)
		result=subprocess_popen(cmd)
		#print(len(result))
		for i in range(len(result)):
			html=result[i]
			stId1=html.find("address")
			if stId1>0:
				break
		if stId1<0:
			return "%s: timeout" % ip
		#print(result)
		#html=result[0]#.encode('utf-8')
		#print(html)
		#stId1=html.find("address")
		addr=html[stId1+9:stId1+30]
		stId2=addr.find("<")
		addr=addr[0:stId2]
		result=ip + "," + addr
		return result
	except:
		return "%s: timeout" % ip
	#print(result)
	#print(result[0]) 
	#res=result[0]
	#if len(res)<2:
	#	return "%s: timeout" % ip
	#else:
	#	return res

def getLogName():
    tt=time.localtime(time.time())
    y=tt.tm_year
    m=tt.tm_mon
    d=tt.tm_mday
    # y=2000
    # m=3
    # d=1
    thirty=[4,6,9,11]
    other=[1,3,5,7,8,10,12]
    if m>1:
        if d==1:
            m=m-1
            if m in thirty:
                d=30
            elif m in other:
                d=31
            elif (y%4==0) and (y%100 !=0) or (y%400)==0:
                d=29
            else:
                d=28
        else:
            d=d-1
    else:
        if d==1:
            m=12
            y=y-1
            d=31
        else:
            d=d-1
           
    filename='frps.'+str(y)+'-'+str(m).zfill(2)+'-'+str(d).zfill(2)+'.log'
    #print(filename)
    return filename
          
 
if __name__ == "__main__":
    logname='/mnt/sda3/log/'+getLogName() #edit this path
    print(logname)
    try:
        f=open(logname)
    except:
        logname='/mnt/sda3/log/frps.log' #and this path
        print(logname)
        f=open(logname)

    logs=f.readlines()
    f.close()
    ips=[]
    for log in logs:
        connId=log.find("connection [")
	#isssh=log.find("[ssh")
        #if connId>0 and isssh>0:
        if connId>0:
            log=log[connId+12:16+connId+12] # to get the full ip string, change 15 to 16
            connId=log.find(":")
            log=log[0:connId]
            #print(log)
            ips.append(log)
    #print(ips)
    #print(set(ips))
    f_cn = open('ip-check-cn.txt', 'w')
    a=u'\u4e2d\u56fd'
    #a是中国的unicode
    f=open('ip-check.txt', 'w')
    #print(type(set(ips)))
    ipNum=len(set(ips))*10
    for ip in set(ips):
        #checkIP(ip)
        for i in range(5):
            line = checkIP2(ip)
            if line.find("timeout")<0:
                break
            else:
                print("time out get again")
                time.sleep(2)
                
        print(line.encode('utf-8')) #为了让openwrt中能正常的打印结果到终端
        if line.find(a)<0:
            f.write(line.encode('utf-8')+'\n')
        else:
            f_cn.write(line.encode('utf-8')+'\n')

        time.sleep(2)
    f.close()
    f_cn.close()
    print("Done")

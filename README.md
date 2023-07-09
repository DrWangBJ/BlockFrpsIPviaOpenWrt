# BlockFrpsIPviaOpenWrt
## 中文版说明：
尝试用lede（openwrt）路由的防火墙来阻止非法的连接。

由于Frps是一个开源的内网穿透工具，很方便的同时，也给不法分子带来了攻击的目标。开放的端口会受到攻击，黑客会使用暴力破解的手段来尝试攻入服务器及客户端。从Frps的dashboard上可以看出一些非法的流量，为了避免被攻陷，一方面提升密保等级，一方面屏蔽攻击者IP。屏蔽IP可以使用防火墙。但是首先要识别到连接的IP，再从中过滤掉想保留的IP，再将识别到的IP添加到防火墙的黑名单中。

在此使用了python作为语言。服务器是布署在lede（openwrt）上，自带的python是2.7版。

### 文件说明：
iploc.py，对frps.log文件进行分析，查找其中的连接的IP，并查询IP的属地信息，将IP和属地信息写入到文件中，其中国外IP写入到`ip-check.txt`中，国内IP写入到`ip-check-cn.txt`中。国外IP不判断，直接屏蔽，国内IP后续判断一下是否为白名单IP。

blockip.py，对查询到的IP和属地信息进行过滤，将所有的国外IP写入到ipset集中，对国内的IP进行白名单过滤，将白名单以外的屏蔽。

whitelist.txt，白名单，格式是一行是一个组合，中间用空格分隔，比如要将所有的北京，联通的IP设为白名单，就要写`北京 联通`，英文空格。这样在过滤时会查找IP和属地信息同时包括`北京`和`联通`的行，不对此行进行屏蔽。

blockip.sh，将命令流用bash的形式写出，先查找IP，再过滤IP并写入到ipset中，最后重启防火墙，使列表生效。


## English Readme：
Attempt to use a firewall with LEDE (openwrt) routing to block illegal connections.

Due to the fact that Frps is an open source intranet penetration tool, it is very convenient and also brings targets for criminals to attack. Open ports will be attacked, and hackers will use brute force to attempt to break into servers and clients. From the dashboard of Frps, it can be seen that there are some illegal traffic. In order to avoid being attacked, on the one hand, the security level is increased, and on the other hand, the attacker's IP is blocked. Blocking IP can use a firewall. But first, you need to identify the connected IP, filter out the IP you want to keep, and then add the identified IP to the firewall's blacklist.

Python is used as the language here. The server is deployed on LEDE (openwrt) and comes with Python version 2.7.
### File info:
iploc.py, analyze the frps.log file, search for the connected IPs, and query the IP's territorial information. Write the IP and territorial information to the file, with foreign IPs written to `ip-check.txt` and domestic IPs written to `ip-check-cn.txt`. Foreign IPs are not determined and are directly blocked. Domestic IPs will be determined later to determine whether they are on the whitelist.

blockip.py filters the queried IP and territorial information, writes all foreign IPs into the ipset set, and performs whitelist filtering on domestic IPs to block those outside the whitelist.

whitelist.txt, a whitelist, formatted as a combination of one line and separated by spaces. For example, if you want to set all Beijing and Unicom IPs as whitelists, you need to write `Beijing Unicom` with English spaces. This way, when filtering, the IP and location information will be searched for rows that include both `Beijing` and `Unicom`, and this row will not be blocked.

blockip.sh, write the command stream in bash format, first search for the IP, then filter the IP and write it to the ipset, and finally restart the firewall to make the list effective.

# BlockFrpsIPviaOpenWrt
## 中文版说明：
尝试用lede（openwrt）路由的防火墙来阻止非法的连接。
由于Frps是一个开源的内网穿透工具，很方便的同时，也给不法分子带来了攻击的目标。开放的端口会受到攻击，黑客会使用暴力破解的手段来尝试攻入服务器及客户端。从Frps的dashboard上可以看出一些非法的流量，为了避免被攻陷，一方面提升密保等级，一方面屏蔽攻击者IP。屏蔽IP可以使用防火墙。但是首先要识别到连接的IP，再从中过滤掉想保留的IP，再将识别到的IP添加到防火墙的黑名单中。
在此使用了python作为语言。服务器是布署在lede（openwrt）上，自带的python是2.7版。

## English Readme：
Attempt to use a firewall with LEDE (openwrt) routing to block illegal connections.
Due to the fact that Frps is an open source intranet penetration tool, it is very convenient and also brings targets for criminals to attack. Open ports will be attacked, and hackers will use brute force to attempt to break into servers and clients. From the dashboard of Frps, it can be seen that there are some illegal traffic. In order to avoid being attacked, on the one hand, the security level is increased, and on the other hand, the attacker's IP is blocked. Blocking IP can use a firewall. But first, you need to identify the connected IP, filter out the IP you want to keep, and then add the identified IP to the firewall's blacklist.
Python is used as the language here. The server is deployed on LEDE (openwrt) and comes with Python version 2.7.


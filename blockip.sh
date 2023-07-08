#!/bin/bash
cd /root
python iploc.py
python blockip.py
/etc/init.d/firewall restart >/dev/null 2>&1
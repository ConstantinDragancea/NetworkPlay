import socket
import traceback
import random
import requests
import json
import struct
import sys

TTL_LIMIT = 15
PORT_LOWER_LIMIT = 33434
PORT_UPPER_LIMIT = 33534

IP2LOC = 'https://api.ip2loc.com/'
IP2LOC_KEY = ''
IP2LOC_API = ''

IP_ADDRS = []

# socket de UDP
udp_send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)

# socket RAW de citire a răspunsurilor ICMP
icmp_recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
# setam timout in cazul in care socketul ICMP la apelul recvfrom nu primeste nimic in buffer
icmp_recv_socket.settimeout(2)

def GetIP(address):
    headers = {
        'Accept': 'application/dns-json'
    }
    response = requests.get('https://1.1.1.1/dns-query?name={}&type=A'.format(address), headers=headers)
    parsed_response = json.loads(response.text)

    try:
        return parsed_response['Answer'][0]['data']
    except:
        return 'Domeniu inexistent!'

def header2dict(names, struct_format, data):
    """ unpack the raw received IP and ICMP header informations to a dict """
    unpacked_data = struct.unpack(struct_format, data)
    return dict(zip(names, unpacked_data))

def get_location_info(ip):
    '''Folositi un API public, cum ar fi cel de la ip2loc pentru
    a afisa locatia despre IP: https://ip2loc.com/documentation'''
    headers = {
        'Accept': 'application/dns-json'
    }
    response = requests.get(IP2LOC_API + ip, headers=headers)
    parsed_response = json.loads(response.text)

    # print(parsed_response)
    oras = parsed_response['location']['city']
    regiune = parsed_response['location']['capital']
    tara = parsed_response['location']['country']['name']
    return ip, oras, regiune, tara

def traceroute(ip):
    global IP_ADDRS
    '''Functie care are ca scop afisarea locatiilor geografice 
    de pe rutele pachetelor.
    '''

    for TTL in range(1, TTL_LIMIT + 1):
        port = random.randint(PORT_LOWER_LIMIT, PORT_UPPER_LIMIT)

        # setam TTL in headerul de IP pentru socketul de UDP
        udp_send_sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, TTL)
        # trimite un mesaj UDP catre un tuplu (IP, port)
        udp_send_sock.sendto(b'ador', (ip, port))

        # asteapta un mesaj ICMP de tipul ICMP TTL exceeded messages
        # aici nu verificăm daca tipul de mesaj este ICMP
        # dar ati putea verifica daca primul byte are valoarea Type == 11
        # https://tools.ietf.org/html/rfc792#page-5
        # https://en.wikipedia.org/wiki/Internet_Control_Message_Protocol#Header
        addr = 'done!'

        data = b"LOL"

        try:
            data, addr = icmp_recv_socket.recvfrom(63535)

            icmp_header = header2dict(
                names=[
                    "type", "code", "checksum",
                    "packet_id", "seq_number"
                ],
                struct_format="!BBHHH",
                data=data[20:28]
                # data=data[:8]
            )
            print(icmp_header)
            IP_ADDRS.append(addr[0])

            if icmp_header["type"] == 3:
                print("Destination reached!")
                break            

        except Exception as e:
            pass
            # print("Socket timeout ", str(e))
            # print(traceback.format_exc())

    for trace_ip in IP_ADDRS:
        print(get_location_info(trace_ip))


def LoadIP2LOC_Key():
    global IP2LOC_KEY
    global IP2LOC
    global IP2LOC_API
    with open('IP2LOC_KEY', 'r') as fin:
        IP2LOC_KEY = fin.read()
    IP2LOC_API = IP2LOC + IP2LOC_KEY + '/'

if __name__ == "__main__":
    adresa = sys.argv[1]
    LoadIP2LOC_Key()

    ip_addr = GetIP(adresa)

    traceroute(ip_addr)
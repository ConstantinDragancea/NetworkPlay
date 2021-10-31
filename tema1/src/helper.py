import struct
import socket
import logging
from copy import deepcopy

MAX_UINT32 = 0xFFFFFFFF
MAX_BITI_CHECKSUM = 16
MAX_SEGMENT = 1400
RELIABLE_UDP_HEADER_BYTESIZE = 8

class SenderPacket:
    def __init__(self, data : bytes, msg_type: str, seq_nr : int):
        self.raw = None
        self.header = None
        self.header_no_checksum = None
        self.data = data
        self.seq_nr = seq_nr
        self.checksum = 0
        
        self.spf = 0b000
        if msg_type == 'S':
            self.spf = 0b100
        elif msg_type == 'P':
            self.spf = 0b010
        elif msg_type == 'F':
            self.spf = 0b001
        else:
            exit(-1)
        
        self.build_packet()
        
    def build_header_no_checksum(self):
        spf_zero = self.spf << 13 # muta cei trei biti cu 13 pozitii la stanga
        self.header_no_checksum = struct.pack('!LHH',
            self.seq_nr, 0, spf_zero)

    def build_header(self):
        self.checksum = CalculateChecksum(self.header_no_checksum + self.data)
        spf_zero = self.spf << 13 # muta cei trei biti cu 13 pozitii la stanga
        self.header = struct.pack('!LHH',
            self.seq_nr, self.checksum, spf_zero)
        
    
    def build_packet(self):
        self.build_header_no_checksum()
        self.build_header()

        self.raw = self.header + self.data
        return

class ReceiverPacket:
    def __init__(self, ack_nr : int, window : int):
        self.raw = None
        self.header = None
        self.header_no_checksum = None
        self.ack_nr = ack_nr
        self.window = window
        self.checksum = 0

        self.build_packet()
    
    def build_header_no_checksum(self):
        self.header_no_checksum = struct.pack('!LHH',
            self.ack_nr, self.checksum, self.window)
        return

    def build_header(self):
        self.checksum = CalculateChecksum(self.header_no_checksum)
        self.header = struct.pack('!LHH', self.ack_nr, self.checksum, self.window)
        return
    
    def build_packet(self):
        # self.build_ipv4_header()
        # self.build_udpheader()
        # self.build_pseudoheader()
        self.build_header_no_checksum()
        self.build_header()

        self.raw = self.header
        return

def compara_endianness(numar):
    '''
    https://en.m.wikipedia.org/wiki/Endianness#Etymology
        numarul 16 se scrie in binar 10000 (2^4)
        pe 8 biti, adaugam 0 pe pozitiile mai mari: 00010000
        pe 16 biti, mai adauga un octet de 0 pe pozitiile mai mari: 00000000 00010000
        daca numaratoarea incepe de la dreapta la stanga:
            reprezentarea Big Endian (Network Order) este: 00000000 00010000
                - cel mai semnificativ bit are adresa cea mai mica
            reprezentarea Little Endian este: 00010000 00000000
                - cel mai semnificativ bit are adresa cea mai mare 
    '''
    print ("Numarul: ", numar)
    print ("Network Order (Big Endian): ", [bin(byte) for byte in struct.pack('!H', numar)])
    print ("Little Endian: ", [bin(byte) for byte in struct.pack('<H', numar)])


# def create_header_emitator(seq_nr, checksum, flags='S'):
#     '''
#     TODO: folosind struct.pack impachetati numerele in octeti si returnati valorile
#     flags pot fi 'S', 'P', sau 'F'
#     '''
#     octeti = struct.pack(..)
#     return octeti


def parse_header_emitator(octeti):
    '''
    TODO: folosind struct.unpack despachetati numerele 
    din headerul de la emitator in valori si returnati valorile
    '''
    seq_nr, checksum, spf = struct.unpack('!LHH', octeti)
    flags = ''

    spf = spf >> 13

    if spf & 0b100:
        # inseamna ca am primit S
        flags = 'S'
    elif spf & 0b001:
        # inseamna ca am primit F
        flags = 'F'
    elif spf & 0b010:
        # inseamna ca am primit P
        flags = 'P'
    return (seq_nr, checksum, flags)


# def create_header_receptor(ack_nr, checksum, window):
#     '''
#     TODO: folosind struct.pack impachetati numerele in octeti si returnati valorile
#     flags pot fi 'S', 'P', sau 'F'
#     '''
#     octeti = struct.pack(..)
#     return octeti


def parse_header_receptor(octeti):
    '''
    TODO: folosind struct.unpack despachetati octetii in valori si returnati valorile
    '''
    ack_nr, checksum, window = struct.unpack('!LHH', octeti)
    return (ack_nr, checksum, window)


def citeste_segment(file_descriptor):
    '''
        generator, returneaza cate un segment de 1400 de octeti dintr-un fisier
    '''    
    return file_descriptor.read(MAX_SEGMENT - RELIABLE_UDP_HEADER_BYTESIZE)


def exemplu_citire(cale_catre_fisier):
    with open(cale_catre_fisier, 'rb') as file_in:
        for segment in citeste_segment(file_in):
            print(segment)

def CalculateChecksum(octeti):
    checksum = 0
    max_nr = (1 << MAX_BITI_CHECKSUM) - 1
    suma = 0

    local_octeti = deepcopy(octeti)

    if len(local_octeti) % 2 == 1:
        local_octeti = local_octeti + struct.pack('!B', 0)
    
    for i in range(0, len(octeti), 2):
        nr = (local_octeti[i] << 8) + local_octeti[i + 1]
        suma = (suma + nr) % max_nr
    
    checksum = (max_nr - suma) % max_nr


    # 1. convertim sirul octeti in numere pe 16 biti
    # 2. adunam numerele in complementul lui 1, ce depaseste 16 biti se aduna la coada
    # 3. cheksum = complementarea bitilor sumei
    return checksum


def verifica_checksum(octeti):
    return (CalculateChecksum(octeti) == 0)
    # if CalculateChecksum(octeti):
    #     return True
    # return False



if __name__ == '__main__':
    compara_endianness(16)
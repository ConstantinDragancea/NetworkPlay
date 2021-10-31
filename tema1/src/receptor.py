# receptor Reiable UDP
from helper import *
from argparse import ArgumentParser
import socket
import logging
import random
import traceback

# logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)
logging.basicConfig(filename='receptor.log', filemode='w', format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)

def main():
    parser = ArgumentParser(usage=__file__ + ' '
                                             '-p/--port PORT'
                                             '-f/--fisier FILE_PATH',
                            description='Reliable UDP Receptor')

    parser.add_argument('-p', '--port',
                        dest='port',
                        default='10000',
                        help='Portul pe care sa porneasca receptorul pentru a primi mesaje')

    parser.add_argument('-f', '--fisier',
                        dest='fisier',
                        help='Calea catre fisierul in care se vor scrie octetii primiti')

    # Parse arguments
    args = vars(parser.parse_args())
    port = int(args['port'])
    fisier = args['fisier']

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)

    adresa = '0.0.0.0'
    server_address = (adresa, port)
    sock.bind(server_address)
    logging.info("Serverul a pornit pe adresa %s si pe portul %d", adresa, port)

    last_seq_nr = 0         # primul seq_nr din window-ul curent
    currWindow = 0          # dimensiunea window-ului curent
    lastWindow = 0          # dimensiunea window-ului trimis catre emitator ultima data

    windowBuffer = dict()   # tinem payload-ul pentru fiecare segment din window-ul curent
    last_seq_written = None
    
    try:
        file_descriptor = open(fisier, 'wb')
        
        while True:
            logging.info('Asteptam mesaje...')
            data, address = sock.recvfrom(MAX_SEGMENT)
            logging.info('Content primit: "%s"', data)

            '''
            TODO: pentru fiecare mesaj primit
            1. verificam checksum
            2. parsam headerul de la emitator
            3. trimitem confirmari cu ack = seq_nr+1 daca mesajul e de tip S sau F
                                cu ack = seq_nr daca mesajul e de tip P
            4. scriem intr-un fisier octetii primiti
            5. verificam la sfarsit ca fisierul este la fel cu cel trimis de emitator
            '''

            if verifica_checksum(data) is False:
                logging.info("Mesajul primit de la emitator a fost corupt!")
                continue
                
            seq_nr, checksum, flags = parse_header_emitator(data[:8])
            payload = data[8:]

            # logging.info('Ack Nr: "%d"', seq_nr)
            # logging.info('Checksum: "%d"', checksum)
            # logging.info('Flags: "%s"', flags)            

            packet = None
            newWindow = random.randint(1, 5)        # noul window pe care il trimit la emitator

            if flags == 'S':
                packet = ReceiverPacket(ack_nr = seq_nr + 1, window = newWindow)

                last_seq_nr = seq_nr + 1
                last_seq_written = seq_nr + 1

            elif flags == 'P':
                if seq_nr > last_seq_written and seq_nr not in windowBuffer:
                    windowBuffer[seq_nr] = payload              

                while last_seq_written + 1 in windowBuffer:
                    last_seq_written += 1
                    file_descriptor.write(windowBuffer[last_seq_written])
                    windowBuffer.pop(last_seq_written)

                packet = ReceiverPacket(ack_nr = seq_nr, window = newWindow)
            elif flags == 'F':
                packet = ReceiverPacket(ack_nr = seq_nr + 1, window = newWindow)
                sock.sendto(packet.raw, address)
                break
            
            else:
                exit(-1)

            mesaj = packet.raw
            sock.sendto(mesaj, address)
        
        windowBuffer.clear()
        sock.close()
        file_descriptor.close()

    except Exception as e:
        logging.exception(traceback.format_exc())
        sock.close()
        file_descriptor.close()
                

if __name__ == '__main__':
    main()

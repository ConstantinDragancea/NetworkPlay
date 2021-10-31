# emitator Reliable UDP
from helper import *
from argparse import ArgumentParser
import socket
import logging
import sys
import random
import traceback
from datetime import datetime

# logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)
logging.basicConfig(filename='emitator.log', filemode='w', format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)

TIMEOUT_LOWERBOUND = 1
TIMEOUT_UPPERBOUND = 20

TIMEOUT = 3 # Stores our Smoothed Round Trip Time (SRTT)
ALPHA = 0.8 # Factor for Smoothing our RTT
INCREASE_CONSTANT = 1.1 # Factor for increasing the timeout, in case of socket.timeout

FINALIZE_TIMEOUT = 60 * 5 # 5 minutes

def smoothTimeout(currentTimeout, currentRTT):
    return max(ALPHA * currentTimeout + (1 - ALPHA) * currentRTT, TIMEOUT_LOWERBOUND)

def increaseTimeout(currentTimeout):
    return min(INCREASE_CONSTANT * currentTimeout, TIMEOUT_UPPERBOUND)

def connect(sock, adresa_receptor):
    global TIMEOUT
    '''
    Functie care initializeaza conexiunea cu receptorul.
    Returneaza ack_nr de la receptor si window
    '''
    seq_nr = random.randint(0, MAX_UINT32 // 2) # TODO: setati initial sequence number
    
    packet = SenderPacket(data = b'start connection', msg_type = 'S', seq_nr = seq_nr)
    mesaj = packet.raw

    while True:

        sock.sendto(mesaj, adresa_receptor)
        
        try:
            data, server = sock.recvfrom(MAX_SEGMENT)

            if verifica_checksum(data) is False:
                #daca checksum nu e ok, mesajul de la receptor trebuie ignorat
                logging.info("Mesajul de confirmare a fost corupt, retrying...")
                continue

            ack_nr, checksum, window = parse_header_receptor(data)

            if ack_nr != seq_nr + 1:
                logging.info("Mesajul are un Acknowledgement Number gresit, retrying....")
                continue

            logging.info('Ack Nr: "%d"', ack_nr)
            logging.info('Checksum: "%d"', checksum)
            logging.info('Window: "%d"', window)

            return ack_nr, window
        
        except socket.timeout as e:
            logging.info("Timeout la connect, retrying...")
            TIMEOUT = increaseTimeout(TIMEOUT)
            sock.settimeout(TIMEOUT)
            # TODO: cat timp nu primește confirmare de connect, incearca din nou



def finalize(sock, adresa_receptor, seq_nr):
    global TIMEOUT
    '''
    Functie care trimite mesajul de finalizare
    cu seq_nr dat ca parametru.
    '''
    # TODO:
    # folositi pasii de la connect() pentru a construi headerul
    # valorile de checksum si pentru a verifica primirea mesajului a avut loc
    
    packet = SenderPacket(data = b'close connection', msg_type = 'F', seq_nr = seq_nr)
    mesaj = packet.raw
    
    began_finalize = datetime.now()

    while True:

        if ((datetime.now() - began_finalize).total_seconds() > FINALIZE_TIMEOUT):
            logging.info("Waited for finalise acknowledgement too much, exiting...")
            return

        sock.sendto(mesaj, adresa_receptor)
        
        try:
            data, server = sock.recvfrom(MAX_SEGMENT)

            if verifica_checksum(data) is False:
                #daca checksum nu e ok, mesajul de la receptor trebuie ignorat
                logging.info("Mesajul de confirmare a fost corupt, retrying...")
                continue

            ack_nr, checksum, window = parse_header_receptor(data)

            if ack_nr != seq_nr + 1:
                logging.info("Mesajul are un Acknowledgement Number gresit, retrying....")
                continue

            logging.info('Ack Nr: "%d"', ack_nr)
            logging.info('Checksum: "%d"', checksum)
            logging.info('Window: "%d"', window)

            return
        
        except socket.timeout as e:
            logging.info("Timeout la disconnect, retrying...")
            TIMEOUT = increaseTimeout(TIMEOUT)
            sock.settimeout(TIMEOUT)

    return


def sendWindow(sock, adresa_receptor, seq_nr, window, file_descriptor):
    global TIMEOUT
    '''
    Functie care trimite octeti ca payload catre receptor
    cu seq_nr dat ca parametru.
    Returneaza ack_nr si window curent primit de la server.
    '''
    # TODO...
    
    segments = []               # payload-ul pentru fiecare segment din window
    segmentSentTime = []        # timpul la care s-a trimis fiecare segment din window
    segmentConfirmed = []       # True / False daca receptorul a confirmat primirea segmentului
    fileFinished = False
    newWindow = window

    for i in range(window):
        segment = citeste_segment(file_descriptor)
        if len(segment) == 0:
            window = i
            fileFinished = True
            break
        segments.append(segment)
        segmentSentTime.append(datetime.now())
        segmentConfirmed.append(False)

    while True:

        nrSegmentsUnconfirmed = 0

        for i in range(window):
            if segmentConfirmed[i]:
                continue

            packet = SenderPacket(data = segments[i], msg_type = 'P', seq_nr = seq_nr + i + 1)
            sock.sendto(packet.raw, adresa_receptor)
            segmentSentTime[i] = datetime.now()
            nrSegmentsUnconfirmed += 1

        if nrSegmentsUnconfirmed == 0:
            break

        for i in range(nrSegmentsUnconfirmed):
            try:
                data, server = sock.recvfrom(MAX_SEGMENT)
                logging.info('Content primit: "%s"', data)

                if verifica_checksum(data) is False:
                    logging.info("Emitatorul a primit un pachet corupt de la receptor!")
                    continue

                r_ack_nr, r_checksum, r_window = parse_header_receptor(data)

                logging.info('Ack Nr: "%d"', r_ack_nr)
                logging.info('Checksum: "%d"', r_checksum)
                logging.info('Window: "%d"', r_window)

                segmentPos = r_ack_nr - seq_nr - 1
                newWindow = r_window


                # In cazul in care primim o confirmare dintr-un window precedent
                if (segmentPos < 0):
                    continue

                if segmentConfirmed[segmentPos] == True:
                    continue

                segmentConfirmed[segmentPos] = True
                elapsedTime = datetime.now() - segmentSentTime[segmentPos]
                TIMEOUT = smoothTimeout(TIMEOUT, elapsedTime.total_seconds())
                sock.settimeout(TIMEOUT)
                
            except socket.timeout as e:
                TIMEOUT = increaseTimeout(TIMEOUT)
                sock.settimeout(TIMEOUT)
                logging.info("Timeout la asteptare confirmare, retrying...")
                
    if fileFinished:
        newWindow = -1

    return seq_nr + window, newWindow


def main():
    parser = ArgumentParser(usage=__file__ + ' '
                                             '-a/--adresa IP '
                                             '-p/--port PORT'
                                             '-f/--fisier FILE_PATH',
                            description='Reliable UDP Emitter')

    parser.add_argument('-a', '--adresa',
                        dest='adresa',
                        default='receptor',
                        help='Adresa IP a receptorului (IP-ul containerului, localhost sau altceva)')

    parser.add_argument('-p', '--port',
                        dest='port',
                        default='10000',
                        help='Portul pe care asculta receptorul pentru mesaje')

    parser.add_argument('-f', '--fisier',
                        dest='fisier',
                        help='Calea catre fisierul care urmeaza a fi trimis')

    # Parse arguments
    args = vars(parser.parse_args())

    ip_receptor = args['adresa']
    port_receptor = int(args['port'])
    fisier = args['fisier']

    adresa_receptor = (ip_receptor, port_receptor)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
    # setam timeout pe socket in cazul in care recvfrom nu primeste nimic in 3 secunde
    sock.settimeout(TIMEOUT)

    try:
        '''
        TODO:
        1. initializeaza conexiune cu receptor
        2. deschide fisier, citeste segmente de octeti
        3. trimite `window` segmente catre receptor,
         send trebuie sa trimită o fereastră de window segmente
         până primșete confirmarea primirii tuturor segmentelor
        4. asteapta confirmarea segmentelor, 
        in cazul pierderilor, retransmite fereastra sau doar segmentele lipsa
        5. in functie de diferenta de timp dintre trimitere si receptia confirmarii,
        ajusteaza timeout
        6. la finalul trimiterilor, notifica receptorul ca fisierul s-a incheiat
        '''
        seq_nr, window = connect(sock, adresa_receptor)
        file_descriptor = open(fisier, 'rb')

        while True:
            # segment = citeste_segment(file_descriptor)
            ack_nr, newWindow = sendWindow(sock, adresa_receptor, seq_nr, window, file_descriptor)
            seq_nr = ack_nr
            window = newWindow

            # veridicam daca a fost trimis tot fisierul si, in caz afirmativ, finalizam conexiunea
            if window == -1:
                break
        
        finalize(sock, adresa_receptor, seq_nr + 1)
        sock.close()
        file_descriptor.close()
    except Exception as e:
        logging.exception(traceback.format_exc())
        sock.close()
        file_descriptor.close()



if __name__ == '__main__':
    main()
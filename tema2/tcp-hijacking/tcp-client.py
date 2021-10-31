# TCP client
import socket
import logging
import time

logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)

port = 10000
adresa = '198.10.0.2'
server_address = (adresa, port)
mesaj = 'MesajOriginal'

def send_once():
    sock.send(mesaj.encode('utf-8'))
    time.sleep(2)
    data = sock.recv(1024)
    logging.info('Content primit: "%s"', data)

try:
    logging.info('Handshake cu %s', str(server_address))
    sock.connect(server_address)
    logging.info('Handshake sucessful!')
    logging.info('Beginning data transmission')
    time.sleep(2)
    while True:
        send_once()

finally:
    logging.info('Closing socket...')
    sock.close()

# TCP Server
import socket
import logging
import time

logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)

port = 10000
adresa = '0.0.0.0'
server_address = (adresa, port)
sock.bind(server_address)
logging.info("Serverul a pornit pe %s si portul %d", adresa, port)
sock.listen(5)

try:
    logging.info('Asteptam conexiuni...')
    conexiune, address = sock.accept()
    logging.info("Handshake successful cu %s", address)
    time.sleep(3)

    while True:
        data = conexiune.recv(1024)
        logging.info('Content primit: "%s"', data)
        print("Incercam sa trimitem raspuns...")
        conexiune.send(b"Server a primit mesajul: " + data)
        time.sleep(2)
finally:
    conexiune.close()
    sock.close()

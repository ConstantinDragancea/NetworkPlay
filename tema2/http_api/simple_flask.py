from flask import Flask, json, jsonify
from flask import request
import socket, struct

def ipToNumber(ip):
    octeti = socket.inet_aton(ip)
    return struct.unpack('!L', octeti)[0]

def numberToIp(nr):
    return socket.inet_ntoa(struct.pack('!L', nr))


def getSubnets(subnet, dim):
    dims = []

    for i, val in enumerate(dim):
        dims.append([i, val])

    # sortam dimensiunile descrescator
    dims.sort(key = lambda x : - x[1])

    maxVal = (1 << 32) - 1
    ip, msk = subnet.split('/')
    totalAddress = (1 << (32 - int(msk)))

    lastIp = ipToNumber(ip)
    answer = {}

    for i, hosts in dims:
        # calculam masca subnet-ului
        bits = 1
        while (1 << bits) < hosts:
            bits += 1
        
        totalAddress -= (1 << bits)
        if totalAddress < 0:
            return ({
                'status': 'failed',
                'erroe_message': 'Not enough nodes for the hosts!'
            })

        answer["LAN" + str(i)] = numberToIp(lastIp) + "/" + str(32 - bits)
        
        invSubnetMask = (1 << bits) - 1
        lastIp = lastIp | invSubnetMask

        if lastIp > maxVal:
            return ({
                'status': 'failed',
                'error_message': 'Not enough nodes for the hosts!'
            })

        lastIp += 1

    return answer
    


app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

'''
This method expects a json content.
Use header: 'Content-Type: application/json'
'''
@app.route('/subnet', methods=['POST'])
def post_method():
    req = request.get_json()
    return jsonify(getSubnets(req['subnet'], req['dim']))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
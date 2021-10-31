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
            return jsonify({
                'status': 'failed',
                'erroe_message': 'Not enough nodes for the hosts!'
            })

        lastIp += 1

    return answer

if __name__ == '__main__':
    print(getSubnets("10.189.24.0/24", [10, 10, 100]))
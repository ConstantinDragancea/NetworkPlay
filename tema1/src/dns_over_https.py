import requests
import sys
import json

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


if __name__ == "__main__":
    # dns_name = sys.argv[1]
    # print(GetIP(dns_name))
    print(GetIP('unibuc.ro'))    
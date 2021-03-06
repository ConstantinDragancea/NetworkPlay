# Soluție

## 1. DNS over HTTPS
Am implementat funcția aici:
```python
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
```
iar aici e un exemplu de execuție
```python
print(GetIP('unibuc.ro'))
# Output: 80.96.21.209
```

## 2. Traceroute

Am implementat soluția iar aici este output-ul:

### Ruta către IP1
```
('10.40.0.2', None, None, None)
('10.40.0.5', None, None, None)
('86.106.27.102', None, 'Bucharest', 'Romania')
('85.186.202.29', 'Ploieşti', 'Bucharest', 'Romania')
('84.116.217.241', None, 'Amsterdam', 'Netherlands')
('84.116.216.253', None, 'Amsterdam', 'Netherlands')
('213.46.170.138', None, 'Amsterdam', 'Netherlands')
('89.149.140.194', 'Torokszentmiklos', 'Budapest', 'Hungary')
('46.33.92.150', None, 'Washington D.C.', 'United States')
('107.155.17.83', 'Paris', 'Paris', 'France')
('107.155.17.130', 'Paris', 'Paris', 'France')
```

### Ruta către IP2
```
('10.40.0.2', None, None, None)
('10.40.0.5', None, None, None)
('86.106.27.102', None, 'Bucharest', 'Romania')
('89.149.30.53', 'Bucharest', 'Bucharest', 'Romania')
('149.6.51.225', None, 'Washington D.C.', 'United States')
('154.54.59.217', None, 'Washington D.C.', 'United States')
('154.54.38.245', None, 'Washington D.C.', 'United States')
('130.117.3.137', None, 'Washington D.C.', 'United States')
('154.54.59.86', None, 'Washington D.C.', 'United States')
('130.117.3.137', None, 'Washington D.C.', 'United States')
('154.54.36.53', None, 'Washington D.C.', 'United States')
('130.117.0.121', None, 'Washington D.C.', 'United States')
('130.117.51.41', None, 'Washington D.C.', 'United States')
('154.54.42.85', None, 'Washington D.C.', 'United States')
('154.54.77.246', None, 'Washington D.C.', 'United States')
('154.54.42.85', None, 'Washington D.C.', 'United States')
('154.54.7.129', None, 'Washington D.C.', 'United States')
('154.54.31.89', None, 'Washington D.C.', 'United States')
('154.54.31.89', None, 'Washington D.C.', 'United States')
('154.54.44.141', None, 'Washington D.C.', 'United States')
('154.54.5.89', None, 'Washington D.C.', 'United States')
('154.54.42.158', None, 'Washington D.C.', 'United States')
('38.104.140.134', 'San Francisco', 'Washington D.C.', 'United States')
('112.190.30.49', None, 'Seoul', 'South Korea')
('112.174.95.54', None, 'Seoul', 'South Korea')
('203.234.255.114', 'Seoul', 'Seoul', 'South Korea')
```

### Ruta către IP3
```
('10.40.0.2', None, None, None)
('10.40.0.5', None, None, None)
('86.106.27.102', None, 'Bucharest', 'Romania')
('89.149.30.53', 'Bucharest', 'Bucharest', 'Romania')
('149.6.51.225', None, 'Washington D.C.', 'United States')
('154.54.59.217', None, 'Washington D.C.', 'United States')
('154.54.38.245', None, 'Washington D.C.', 'United States')
('130.117.3.137', None, 'Washington D.C.', 'United States')
('154.54.59.86', None, 'Washington D.C.', 'United States')
('154.54.58.5', None, 'Washington D.C.', 'United States')
('154.54.36.53', None, 'Washington D.C.', 'United States')
('154.54.58.238', None, 'Washington D.C.', 'United States')
('154.54.27.169', None, 'Washington D.C.', 'United States')
('154.54.80.2', None, 'Washington D.C.', 'United States')
('38.104.75.98', 'Hawthorne', 'Washington D.C.', 'United States')
('58.138.81.53', None, 'Tokyo', 'Japan')
('58.138.81.210', None, 'Tokyo', 'Japan')
('58.138.81.49', None, 'Tokyo', 'Japan')
('58.138.89.145', None, 'Tokyo', 'Japan')
('58.138.120.14', None, 'Tokyo', 'Japan')
('58.138.89.145', None, 'Tokyo', 'Japan')
```


## 3. Reliable UDP

Log-urile sunt truncate in acest readme. Pentru log-urile integrale, vedeti [src/emitator.log](https://github.com/nlp-unibuc/tema1-807/blob/master/src/emitator.log) și [src/receptor.log](https://github.com/nlp-unibuc/tema1-807/blob/master/src/receptor.log)

Am executat emițătorul cu:
```sh
python3 emitator.py -a 198.8.0.2 -p 10000 -f imagine.jpeg
```

și receptorul cu:
```sh
python3 receptor.py -p 10000 -f primesc.jpg
```

din directorul **./src**. Practic, emițătorul trimite receptorului imaginea **imagine.jpeg**, o imagine Full HD de peste **400kb**. La sfârșit rulăm, din același director:
```
python3 verify_files.py imagine.jpeg primesc.jpg
```
și primim output-ul:
```
Fisierele sunt egale!
```
Deasemenea, putem deschide imaginile **primesc.jpg** și **imagine.jpeg** ca să vedem că sunt la fel.

### Emițător - mesaje de logging
Rulăm `docker-compose logs emitator` și punem rezultatul aici:
```
....
[LINE:226]# INFO     [2021-04-05 15:11:56,563]  Window: "4"
[LINE:197]# INFO     [2021-04-05 15:11:56,563]  Content primit: "b'\x12\xc0wuu\xc8\x00\x02'"
[LINE:224]# INFO     [2021-04-05 15:11:56,564]  Ack Nr: "314603381"
[LINE:225]# INFO     [2021-04-05 15:11:56,564]  Checksum: "30152"
[LINE:226]# INFO     [2021-04-05 15:11:56,564]  Window: "2"
[LINE:197]# INFO     [2021-04-05 15:11:56,569]  Content primit: "b'\x12\xc0wvu\xc6\x00\x03'"
[LINE:224]# INFO     [2021-04-05 15:11:56,574]  Ack Nr: "314603382"
[LINE:225]# INFO     [2021-04-05 15:11:56,574]  Checksum: "30150"
[LINE:226]# INFO     [2021-04-05 15:11:56,574]  Window: "3"
[LINE:197]# INFO     [2021-04-05 15:11:56,672]  Content primit: "b'\x12\xc0wxu\xc2\x00\x05'"
[LINE:224]# INFO     [2021-04-05 15:11:56,685]  Ack Nr: "314603384"
[LINE:225]# INFO     [2021-04-05 15:11:56,685]  Checksum: "30146"
[LINE:226]# INFO     [2021-04-05 15:11:56,685]  Window: "5"
[LINE:197]# INFO     [2021-04-05 15:11:56,685]  Content primit: "b'\x12\xc0wwu\xc4\x00\x04'"
[LINE:224]# INFO     [2021-04-05 15:11:56,686]  Ack Nr: "314603383"
[LINE:225]# INFO     [2021-04-05 15:11:56,686]  Checksum: "30148"
[LINE:226]# INFO     [2021-04-05 15:11:56,686]  Window: "4"
[LINE:197]# INFO     [2021-04-05 15:11:56,792]  Content primit: "b'\x12\xc0wzu\xc3\x00\x02'"
[LINE:224]# INFO     [2021-04-05 15:11:56,802]  Ack Nr: "314603386"
[LINE:225]# INFO     [2021-04-05 15:11:56,802]  Checksum: "30147"
[LINE:226]# INFO     [2021-04-05 15:11:56,802]  Window: "2"
[LINE:197]# INFO     [2021-04-05 15:11:56,812]  Content primit: "b'\x12\xc0w{u\xc0\x00\x04'"
[LINE:224]# INFO     [2021-04-05 15:11:56,818]  Ack Nr: "314603387"
[LINE:225]# INFO     [2021-04-05 15:11:56,818]  Checksum: "30144"
[LINE:226]# INFO     [2021-04-05 15:11:56,818]  Window: "4"
[LINE:197]# INFO     [2021-04-05 15:11:56,828]  Content primit: "b'\x12\xc0w|u\xc0\x00\x03'"
[LINE:224]# INFO     [2021-04-05 15:11:56,833]  Ack Nr: "314603388"
[LINE:225]# INFO     [2021-04-05 15:11:56,833]  Checksum: "30144"
[LINE:226]# INFO     [2021-04-05 15:11:56,833]  Window: "3"
[LINE:231]# INFO     [2021-04-05 15:11:57,840]  Timeout la asteptare pentru confirmare, retrying...
[LINE:197]# INFO     [2021-04-05 15:11:58,886]  Content primit: "b'\x12\xc0wyu\xc5\x00\x01'"
[LINE:224]# INFO     [2021-04-05 15:11:58,891]  Ack Nr: "314603385"
[LINE:225]# INFO     [2021-04-05 15:11:58,891]  Checksum: "30149"
[LINE:226]# INFO     [2021-04-05 15:11:58,891]  Window: "1"
[LINE:231]# INFO     [2021-04-05 15:11:59,985]  Timeout la asteptare pentru confirmare, retrying...
[LINE:197]# INFO     [2021-04-05 15:12:00,323]  Content primit: "b'\x12\xc0w}u\xbe\x00\x04'"
[LINE:224]# INFO     [2021-04-05 15:12:00,323]  Ack Nr: "314603389"
[LINE:225]# INFO     [2021-04-05 15:12:00,323]  Checksum: "30142"
[LINE:226]# INFO     [2021-04-05 15:12:00,323]  Window: "4"
[LINE:197]# INFO     [2021-04-05 15:12:00,425]  Content primit: "b'\x12\xc0w\x7fu\xbb\x00\x05'"
[LINE:224]# INFO     [2021-04-05 15:12:00,425]  Ack Nr: "314603391"
[LINE:225]# INFO     [2021-04-05 15:12:00,425]  Checksum: "30139"
[LINE:226]# INFO     [2021-04-05 15:12:00,425]  Window: "5"
[LINE:197]# INFO     [2021-04-05 15:12:00,425]  Content primit: "b'\x12\xc0w\x80u\xbb\x00\x04'"
[LINE:224]# INFO     [2021-04-05 15:12:00,425]  Ack Nr: "314603392"
[LINE:225]# INFO     [2021-04-05 15:12:00,426]  Checksum: "30139"
[LINE:226]# INFO     [2021-04-05 15:12:00,426]  Window: "4"
[LINE:197]# INFO     [2021-04-05 15:12:00,440]  Content primit: "b'\x12\xc0w~u\xc0\x00\x01'"
[LINE:224]# INFO     [2021-04-05 15:12:00,448]  Ack Nr: "314603390"
[LINE:225]# INFO     [2021-04-05 15:12:00,448]  Checksum: "30144"
[LINE:226]# INFO     [2021-04-05 15:12:00,448]  Window: "1"
[LINE:197]# INFO     [2021-04-05 15:12:00,458]  Content primit: "b'\x12\xc0w\x81u\xbd\x00\x01'"
[LINE:224]# INFO     [2021-04-05 15:12:00,464]  Ack Nr: "314603393"
[LINE:225]# INFO     [2021-04-05 15:12:00,464]  Checksum: "30141"
[LINE:226]# INFO     [2021-04-05 15:12:00,464]  Window: "1"
[LINE:197]# INFO     [2021-04-05 15:12:00,533]  Content primit: "b'\x12\xc0w\x82u\xb8\x00\x05'"
[LINE:224]# INFO     [2021-04-05 15:12:00,538]  Ack Nr: "314603394"
[LINE:225]# INFO     [2021-04-05 15:12:00,538]  Checksum: "30136"
[LINE:226]# INFO     [2021-04-05 15:12:00,538]  Window: "5"
[LINE:197]# INFO     [2021-04-05 15:12:00,644]  Content primit: "b'\x12\xc0w\x87u\xb3\x00\x05'"
[LINE:224]# INFO     [2021-04-05 15:12:00,681]  Ack Nr: "314603399"
[LINE:225]# INFO     [2021-04-05 15:12:00,681]  Checksum: "30131"
[LINE:226]# INFO     [2021-04-05 15:12:00,681]  Window: "5"
[LINE:197]# INFO     [2021-04-05 15:12:00,686]  Content primit: "b'\x12\xc0w\x84u\xb8\x00\x03'"
....
```


### Receptor - mesaje de logging
Rulăm `docker-compose logs receptor` și punem rezultatul aici:
```
[LINE:37]# INFO     [2021-04-05 15:11:46,651]  Serverul a pornit pe adresa 0.0.0.0 si pe portul 10000
[LINE:50]# INFO     [2021-04-05 15:11:46,651]  Asteptam mesaje...
[LINE:52]# INFO     [2021-04-05 15:11:48,422]  Content primit: "b'\x12\xc0w.\x91\xf0\x80\x00start connection'"
[LINE:50]# INFO     [2021-04-05 15:11:48,422]  Asteptam mesaje...
[LINE:52]# INFO     [2021-04-05 15:11:48,423]  Content primit: "b'\x12\xc0w0\x0bp@\x00\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xe2\x02\x1cICC_PROFILE\x00\x01\x01\x00\x00\x02\x0clcms\x02\x10\x00\x00mntrRGB XYZ \x07\xdc\x00\x01\x00\x19\x00\x03\x00)\x009acspAPPL\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf6\xd6\x00\x01\x00\x00\x00\x00\xd3-lcms\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\ndesc\x00\x00\x00\xfc\x00\x00\x00^cprt\x00\x00\x01\\\x00\x00\x00\x0bwtpt\x00\x00\x01h\x00\x00\x00\x14bkpt\x00\x00\x01|\x00\x00\x00\x14rXYZ\x00\x00\x01\x90\x00\x00\x00\x14gXYZ\x00\x00\x01\xa4\x00\x00\x00\x14bXYZ\x00\x00\x01\xb8\x00\x00\x00\x14rTRC\x00\x00\x01\xcc\x00\x00\x00@gTRC\x00\x00\x01\xcc\x00\x00\x00@bTRC\x00\x00\x01\xcc\x00\x00\x00@desc\x00\x00\x00\x00\x00\x00\x00\x03c2\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00text\x00\x00\x00\x00IX\x00\x00XYZ \x00\x00\x00\x00\x00\x00\xf6\xd6\x00\x01\x00\x00\x00\x00\xd3-XYZ \x00\x00\x00\x00\x00\x00\x03\x16\x00\x00\x033\x00\x00\x02\xa4XYZ \x00\x00\x00\x00\x00\x00o\xa2\x00\x008\xf5\x00\x00\x03\x90XYZ \x00\x00\x00\x00\x00\x00b\x99\x00\x00\xb7\x85\x00\x00\x18\xdaXYZ \x00\x00\x00\x00\x00\x00$\xa0\x00\x00\x0f\x84\x00\x00\xb6\xcfcurv\x00\x00\x00\x00\x00\x00\x00\x1a\x00\x00\x00\xcb\x01\xc9\x03c\x05\x92\x08k\x0b\xf6\x10?\x15Q\x1b4!\xf1)\x902\x18;\x92F\x05Qw]\xedkpz\x05\x89\xb1\x9a|\xaci\xbf}\xd3\xc3\xe90\xff\xff\xff\xdb\x00\x84\x00\x05\x06\x06\x07\t\x07\n\x0b\x0b\n\r\x0e\r\x0e\r\x13\x12\x10\x10\x12\x13\x1d\x15\x16\x15\x16\x15\x1d+\x1b \x1b\x1b \x1b+&.&#&.&D6006DOB?BO_UU_xrx\x9c\x9c\xd2\x01\x05\x06\x06\x07\t\x07\n\x0b\x0b\n\r\x0e\r\x0e\r\x13\x12\x10\x10\x12\x13\x1d\x15\x16\x15\x16\x15\x1d+\x1b \x1b\x1b \x1b+&.&#&.&D6006DOB?BO_UU_xrx\x9c\x9c\xd2\xff\xc2\x00\x11\x08\x04\xe7\x07X\x03\x01"\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x1d\x00\x00\x01\x05\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00\x01\x02\x03\x05\x06\x07\x08\t\xff\xda\x00\x08\x01\x01\x00\x00\x00\x00\xf9\xfd$\x92QN\x99$\x92I$\x92I$\x9d$\xe9:d\x92N\x93\xa4\x92L\xe9;;\'I\'I\x99\xd3\xbb;\xa7{nj\x19E&L\xe92wd\xd2\x8b\xa4\x9d\xdd\xd2L\xec\x99;\xb2d\x92t\x93;\xa5\'N\xa4\xa2\xec\x9d\xd9I\x99$\x9d\xd9:I$\x99\xd2vI$\x92L\xec\xc93\xc5$\x92I2I&d\xee\x92I3$\x84L\xe9$\x92L\x92I$\x99\'N\xc9:I\'I$\x92t\x92N\x93:I\xd9\xd2gL\xe9\xd2N\x9d\x9d)FM9\xbd\xb1\xa9\xa2\x94RN\xc9\x9d$\x99\'d\xef$\x92gL\xa4\x992vt\x92I;\xb4\xa4\x93\xa4\xd2QRd\xec\x93\'I:I&t\x9d$\x92I$\x93$\x992I3\xb2d\x92I2I$\x92I$\xcc"I$\x92I$\x92I$\xce\x92I:vt\x92N\x92I$\x92t\x92I\xd2t\x92L\xe9\xd4\x9aI\xd3\xb2S\x92Jj\xa6\xb2\x84\xce\xc9$\x92I\xe2\x93\'i;\xa6I$\x9d\'d\xe9\x92I$\xee\xa4\xee\x9d$\x9e.\x99$\xe92t\x92I$\x9d$\x9d\x92I$\x92L\x92I\x92d\x93\'ft\xc9$\x93$\x92vI\x08\xc9;2I$\x92N\x93$\x9d$\xe9$\xe9\'I\xd9$\x92t\x93\xa4\xe9:I\xd3\xa6\x92d\xee\xf2O$\x93:y<\xab\xbe\x15\xbc\x1a\r\x14\xc9\xd3&vM&d\xce\x9d\xd3\'gd\x9d\xe4\x99$\xc9%$\x92wwt\xec\x99\x93\xbaI3\xa4\x92I$\x93\xa4\xe9\xd9$\x99$\x92I\x92I$\xcc\x92I$\xcc\x9d$\x99$\x92I\x90\x892N\x99&I\'t\xc9:I\'I\xd2N\x9d\'I$\x93\xa7I\xdd;\xa4\x94\x99\xe4\x92t\xea\xcbn#B\x99\x966d\x90\xb3\x90\xee\xa0\xa0\xd3\x8d\x0c\xa2\xe9&L\xcc\x93\xa4\xc9\xd9\xd9\xd2fN\x9d\xdd\x92I$\xee\x92I\xdaI:gII$\x99\xd2N\xce\xc9\xd2I\xd2t\xce\x92\x8aI$\x92d\x92I3$\x92I$\x92L\x99$\x93\xb2a\x12I&I$\x9d$\x92N\x92t\x9d$\xe9\xd4\x9d\xd3\xa4\x92I\xd3\xc9\x9d\xddI\xe7(\xda\xd6\x17\x04\xcd&3\xa1,\xa3\x8dd(\x91\x83\xdb\x1c\xb9\xf3\x98p\x85Sfd\x94\x9a,\xcc\x99(\xa4\xc9\xd93\xb3:I\xd9\xd3\xa4\x92t\xe9$\x9d$\x94\x93\'N\xe9$\x92I\xd2I:I\xd2I$\x93$\x92L\x92d\x99\xd2d\x99$\x92I$\x99\xd9\x92I$\xe1$\x93\xa6I$\x9d\'d\xe9\'I:t\x9d'"
[LINE:50]# INFO     [2021-04-05 15:11:48,423]  Asteptam mesaje...
[LINE:52]# INFO     [2021-04-05 15:11:48,423]  Content primit: "b'\x12\xc0w1\x01\xd2@\x00;\xcaO\'t\xc9\x9d\'w\x93\xdd+/\xbbY\xe9\x91Z\x9a\xe0\x82a\xc1\x87\xbd\xbaE\x97M)\xa6\x9c\xde\x10\x9e\x0e\x05\x83\xd7\x8c/0nh\xaf\x14\xcd\x16L\xef\x16f\x8b\xb2IE:vI\xa4\xce\x9d\x9d$\xe9:I$\xe9\xd9\xd3\xbaI$\x93\xa4\xe9:I$\x92I$\x92I2I\x92L\x92gL\x92L\x92I$\x99\x92I$\x84I$\xe9\x92I\'N\x92t\x93\xa4\xe9\xd3\xbb\xbc\x9es\x94\xa4\x99\x993\xbb\xd8~\x91\x05j5\xc6QAz\xc5\x1e\xa5;$\xe4\x15d\xe59I\xe6\xee\xee\xa4\xaa\x8b\xbci\x1ca\xc2\xc4\xe5BU\x8d\xcc\x06\xa1$\x9a-\x18\xca1N\xd1t\xce\xec\x9d$\xe9&wI\xd2I)$\x92wI$\x9d:N\x93\xb2t\x92I&I$\x92I&I2I2I$\xc9&I$\x992I$#\xa4\x92t\x92I\'I\'I\xd3\xa4\xee\xee\xf2yNwX\xf7\xa8\xb8\xea\xc9\x99\xa2\\\xf446I\xa6\xf3][u\xd6N\xcb,R\xb6\xc9\xd9e\x8dc\xcd:R\x92d\xea0xSJ\xaa\xa8R&\x06\x10\xe1bd\x850\xf3\xa3\x15\x18\xa6vQt\x92N\x92N\x92I\xd2I:vt\xed$\x92N\x93\xbaN\x92I$\x92I$\xc9\xd2L\x9d2I3$\x93$\x92I&L\x92I3$\x92\x19$\x92I:N\x92N\x92t\x9d:\x92\x93\xbc\xa7;-"\xfb\xb5\xac\xa0Qfd\t#`\xe3\xf4\x8c\xb5L\x8b-\xb2\xcb^S\x9d\xae\xf6\xa9\xda\xe9\x9a\xcb\xac\x95U93Sw\x8cc\x17\xaa\r\n\xe3\x01\xea\xa6\x801\xb9\xc0D\xc0\x17\x9c\xa2\xb6g\xb6\x84\xc9\'I\xd2I$\x93\xa7N\x93:N\xd2d\x9d\'I\xdd:I$\x92I;$\x92I\xd3$\x92L\x92fvI$\x99$\xce\xcc\x92I&d\x93\x8c\x9d$\x92I\'I\'N\x92wN\xee\xf2\xb2J\xeb/.\xcb\x0e<\xb2\xe7\\\xaa!OKP\xcb\'}\xb6\xdb9\xce\xd9X\xf3\xbaPgi[4\xf0W\xdf*T\xe5c\xcam\x17\x82\x9a\x84\xddV\xd0\xaa\xbai\xa4\x1c\x9c\\Jy\xde3*\xa7y\xce\xbae\\\x9d3$\x92t\x92wI\'I\x9d$\x93\xb3\xbawN\x93\xb2I$\x92I;$\xee\xc9$\xc9$\x93$\x99\x92I&I$\xcc\x92I&d\xee:I$\x92N\x92t\x93\xbaI\xdd;\xa9N\xeb\xe7u\x84\x14Y\'\x1d}\xc6\xdfb\xb9\xad&\xd9\xcew\xce\xfb\xa5;/\x94\xde\xc6f\x93\xd7\x0b%}\x93t\x9e\xc9<\x9d\xef\x9a\xb6\x14M$\xf1\x9dqPQ\x1a\x91\xaa\x17/+\'\x94\x0f\x85\xcd\xaeD\xca\x82\xa9aS4Y\xd9;$\xee\x93\xa4\x9d$\x92I\'N\xe9\'I$\x92I$\x92wI$\x92L\x99$\x93$\x99\x92I$\xc9\x9d\x93$\x92L\x9dP\xa4\xc93\xa4\x92t\x9d$\xe9\xd2\x92ww\x95\xd7\x98\\\xca\xbc\x8d\r"\xce&\xdb\xae\x9c\x9d\x95\x96Ye\x84J\xcb.\x9b\xc1]6\x93\xdb8%sJR\xb2j\xc6\xb1\xdd]tg5d\xabx2d\x87\xad\xda\x14\n5\x00\x03\x9c??\xe7\xb8\xa0\xde|\xef|\x8cj\xd3E\x93\xb2N\x92N\xe9$\x9d&I\'N\xe9:I$\x92I;$\x94\x92I$\x92I\x99$\x92L\x932I&vd\xec\x99$\x92J\xa4\x92I$\xe9$\x9d\'I\xdd\xd4\xa6\xec\xf3\xb2\xf34\x0c&\xf24\x8f8\x83\x08\x94\x9d\xe4\xa5m\x8aS\x94\xecI\xa2\x9eWJ\xd5e\xb6X\xf2\x9d\x93x\xa4\x9a\x0f\n\xda\xc5m\xb7\x90D\xee\xb1\xde\xb8\xb2\xad\xa6\xf4\xe6\xd0<(\x12\x8a0\xf0\xb9\xec\x0b\x05g\xca\xc6\x16\xba\xda,\xe9$\x93\xa7I\xd2I$\x92I:t\xe9$\x92I$\x92II$\xce\x93\xa6I3$\x92I2L\xc9\xd9&vL\xec\x99$\x92\x82I$\x92I\'I\xd2wi\xb4\xa7}\x90\x99\x13*\xf4n\xb6\x81\xc6\x96I\x04Y7g\x94\xac\xb2/d\xde\xd9\xcajn@\xcc\xa5\t\\E\x96J\xcb#{I\x9e\x15\xa8\xdd}C\xc5Ym\xb5\x91\x1b\x8b\x92VZ\xf1f\xa4j\x05\x1e\x14\x8f\x91\x9f\x9b\x93\x98\x06\x08c\x06\x1d`\xd6\xd1I\x92N\xec\xe9\xd2I\'L\x92JI\'I$\x92I$\x92JI&t\x9d2I&d\xec\x92L\x92gJ)3\xb2d\xec\xc9%\x14\x92I$\x9d\'I\xd2wN\x9e\xc2\t\xaaD\xc8\xf2\xef\xb4\xbd#t\x0c$\x8b^N\xf2y\xcdJ\xd9[b\x94\xad\xb2SM\t+\xae\xb2jE_cY7\x93\xbc\x93\xcaHh\xd7\x1a\x90\x83\x0e\x9d\xed\x95\xe5\x17u\x92j\xea\x17=\x9e\xb123\x87\xc8\xca\xc6\xc9\x8ePc\xe5\x89\x08\xc5\xd3;\xb2N\x9d:t\x92QI;\xa4\xe9&I\xd2I$\x92JI$\x92t\xc9$\x92\x8aI$\x99$\x92J)2I\x93\xb3$\x92I$\x93\xa4\x9d\'I\xdd\xdd\xe7e\x96\x96\xa7iF\x10I&\x17\xa0aDJS\x94\xa7;&\xa5)<\xa7+\'e\x8e\xce\xf6Ns\x93Yu\xd7\xd8\xa4\xeaSy\xc9\xec\xb5\xd3\xa4\xd4\xc2\x0c\xcc\x86\x00A\xe9,\xadG\xb1\xeb\x18Z^\xbaB\x07?#\x17\x18<\xb0G\xcb\xcc\x16\r\x17M$\x93\xa4\xa4\x92I$\xcc\xee\xce\x9d$\xc9:I$\x92JI$\x92N\xec\xc9\xde)$\xcc\x92I2I3\xa6d\x93$\x93&\x92I$\x92t\x93\xa7I\xdd\xe6\xf2\x94\xe7%iW\xe9[i\x85\x13y%\xdd}\xe4\xcen\xec\xf7Yd\xa4\xf3\xb2V\xd9;$\xa6\xf3\xbaI\xe7)\xdd|\xe4\xd3S\x92\x94\xe5l'"
[LINE:50]# INFO     [2021-04-05 15:11:48,424]  Asteptam mesaje...
[LINE:52]# INFO     [2021-04-05 15:11:48,424]  Content primit: "b'\x12\xc0w2\xfa\xb0@\x00\xdd<\xa5$\xf2\x92\x9c\x94D\x03?6\x8a\xd4\xf4\x8d\xae,\x14U\x14\x0b\x9b\x87\x85\x8f\x960y\xb9\x19\x94A3\xb3\xa4\xe9\'t\x92I$\x92I:I$\x92I$\xec\xee\x93:I;\xa4\xce\x99<RI\x93$\x92d\x92I3$\x93$\xcf$\x92I$\x9d)$\xe9\xe4\xa6\xf2\x94\xe7x\xad"J\x9c\xb5\x8a\xd0\xbc\x83\x1c\x82O\xb54Zd[u\x93\xba\xc7{-\x9d\xb6<m\x9d\xee\xd3\xb1\xee\xbe\xc9\xa9;M\xe5k]4\xedd\x9e/\'\x93\xbaub\xacA\x84\x18Q\xcc.\x10\xa8h5c\x0f\x9b\x8d\x81\x96\x16^fFV}Pe&I\xdd;\xa4\x9d$\x92d\x92t\x92I\'I$\x93\xa4\x92I:t\xc9\xd2L\xec\x99$\xc9\x92I&I$\x93&I2V\xa4\x92I$\xe9:wwR\x94\xa5%acV\xd6\xe8\xa6#F\xd2\xce\xbae\x17\xa4S\xc1\xa7;\xae\xb6v\xdbbV\xdd+/\x93\xd9m\xce\xea\xe2m\x9c\xa4\xf3\x9c\xac\xb2sj\xd4\xack$\xd4\xb4\xdeJ\xb9II\xe4\xf0\xae\x81\xc6f\xaa4\xd44cP\xf4\xe7\x81\xce\xe3\xe6eg\xe2\xe3\x05[E\xdd\x9d:wI:I$\x92I\'I$\x9d$\x92I$\x9d:d\xe9$\x92I\x93\xb2d\x99$\xc9$\xc9$\x92fI&!$\x93:I\xd2\x92N\xee\xee\xa4\xee\xd6]u\xb3\x95\xad+\xae{\x08/^\xf3/.\xe7\x9c\xed\xbe\xd9\xdbd\xe7%u\xd6\xd9d\xc9\xbeS\xb6s\xb2\xd7\x9d\x84]\x9fZ\xba\xc9\x1d1\xea\xb2i\xcb\xa0Wu&\xae\xc5_"gR\xec\x99S]T\xd1\n\xe8\x1e\x10\x1a\xa8\r\x93\x83\x83\x8bN7=\x8c2\x83\'I\xd2wI:I$\x92N\x9d$\xce\x92N\x92I$\x92N\x92I$\x92I&vd\x92d\xc9$\xc9$\x92d\x99"\x92I$\x92N\xe9\xd3\xbb\xa4\xe9\xdeN\xeaM+$E\xf6\xdca\xfaeH\x8bL*\xcb.(\x95;\xec\x95\x93\x9d\xd6M\xec\xb0\x9bem\x97J\xc9\xca\xc2\xec\xaf\x11\xa6\xefd\xec\x94\x88\x92W!Y\xd9\x80\xaa\xbe{\xcb>~\xd3\xfb\x1b\xb6t\x9d(\xd68\xf0\xa6\x81\xa3\x11i\x80\xd9\xf8\xf8\xb9\x18XX\x19c\xc1\x99\xd9:N\xe9\'I$\x92I\xdd$\xec\xe9\'I$\x92I$\x92N\x92I$\x92d\x99\x92I2d\x92d\x92L\xe9\x921&I$\xee\xce\xe9;\xa7O$\xee\xee\xe9\x9eS\x9c\xc9,\xbd\x8d[\xaey\x93y3\xba\xe3m\xb2\xcb,gV\x13d\xe6\xf6\xddl\xe7e\x84Y;\n"\xdc1l\xb6\xebl\x9cZM8\xc2\x13\x8dq\x90@\x01\x99\xc6y\xc6f\xa7k\xee:\xae\xf6A\xda-E5B\x81#\x11\xa9\x88\x80\x81\x89\xcf\xe0\xe1\xe1\xe5\x8bT\x1d\x93\xa4\xee\x92t\x92I$\xa4\x9d:L\x93\xa4\x92N\xc9:I$\x92I$\x92I&gfI$\xc9\x92I2I3\xa4s$\x92N\x92N\x9d\xdd\xd3\xbc\x93\xcaJ/\xa7hT<\xca\xdf\xd4<\xe2/\xa6v\xdbl\xad\xbc\xb2l\xb2jsR\xb6\xdbel\xa5m\x96N\xcb\xd4\xed\xbc\xa1D\xb0\x93\xefww\x84G\x1c3,\x85U\xd0 \xc3P\x0f5\xc4\xd3\xd3ki\xf6\x1a\x11\xb2\xfb&\xcd\x16\xa6\xb8@Z\xe8\xa2\xba\x05\x177\x17\x9e\xc4\xc9\xc1\xc8\x06\xb6d\xe93\xbb:t\x93\xa6N\x9d;\xa4\x9d\x92N\x92I$\x92I$\x92I$\x92I&I\x99$\x99\xd92I&I$\xda,\x93\xa4\x93\xb2wwN\xe9\xe5$\x9dJ2\xea\xf6jh\xde?AiDMFi\xd4\xad\x99\x05\x13u\x8fd\x9eS\xb6\xe7\xb1J\xdb\xec\x93=nD\xe5u\xe5\x1aL\xe5&\x8d\x15\x0f]ms\x8fH\xe3P=4gbg_\xa2M\xe6jk\x93E\xb6Z\x9a\x15\xb5u\xd3U\x03\xd6(b\xe6\xe1a\xe4\xe2cc\x05S\xc1\xdd\x99\xd9$\x9d$\x92t\xe9\xdd$\xe9\x9d$\xe9$\x99$\x92I$\x92I$\x92I2L\x99$\x99$\xc9$\xc9%\xa2\xe9\x9d;)\'N\xe9\xd2wwRW\xc6\xe2\xb7w\xc82\xe7fk,\x99\xf2\x1e\x88<\xe5;\x8c$\x9b,\x9c\xdd\xd4\xed\xb2VZ\xf7\x11\x18(\xa6\x91g\x12I\xf6\xd9$\xa2 \xd5V\xa2\xd3\xa6\x9a\x07\x1e\xa1\xe8\xa6\xa1h\xa6\xc9\x95a[:\xc4F2\x8cc\x08B\x15\xc2\x9a(\x100qp\xb3q\xb9\xbc\x81F\xa6\x11u\x14\x93$\xe9$\x92wN\xe9\'I$\xe9\xd2I\x92d\x92I$\x93\xb2vvI$\xc9$\xcc\x92L\xec\xc9$\x99-4\xf1u\'N\xcf\'\x8b\xa7ww\xba\xfb*\xb0\xad\xf2\xed\xd2,\x9b]\xaa{g\xa4c\xc34H\xc9N\xd2\n$\x9b\'):y[i\x17\xdb\x1b\xa3CZ\xca%\x9aYf\x13c\xba\x8dtSL!\x17\x1czj\xaa\x9a\x84\xaa\x81\xe8\x85R \xd8\x85\xa9\xd6\xe8\xc6\xa8\xa8B\xa6\x8d)\xe2(\xc0\x83\x95\x81\x99\x93\xcb\xe6\x8dM#\x00\x933;$\xe92t\x94\x93\xbaN\xce\x92wI$\x92L\x92I\xd9&RgL\xf1I$\xc9$\x932I&L\x92Ij3\xbb\xc9\x99\xdaO\'L\x9d)XM\xc5L--\xcd\x85q$IE\x17\xa5m\xea\xd9\x0bEa\x8b;\x08*\xf2/\x9b\xbd\x8e\x9a\xd2\xc8\xbd\x9a\xca\x84\xb6\xeb\x19L\xdd\x12L*sI\x9a\xaa\xeb\x84)\x85CWM5@jG\xcd\x94\xe8\xad\xca6"jtf\xba\x8dUWL\x19\xdaQ\xa0 s22syq\x02\xcf\x1e\x80\x84h\xd6\xc9\x92t\x99:N\xee\x9d\'\x8b\xbb\xa7I$\x92I3\xa4\x92L'"
[LINE:50]# INFO     [2021-04-05 15:11:48,424]  Asteptam mesaje...
[LINE:52]# INFO     [2021-04-05 15:11:48,424]  Content primit: "b'\x12\xc0w3\xaf\xba@\x00\xc9\xdd$\xa2\x92I2I$\x99&I&d\x92\xd5N\xe9\x99<\x9eO\'I;L\x8b\xd4\xafb\xba\rX\xcc\xcb\xae\xbe3/@\x8b\xa2\xe9QT\x02\x19Yy\x04\x11d\x9eSLIv4\x9e\x144\xe7d\xa7ag\x16YV\xd8\xc9(A\xa9\xa6\x8ai\xad\x86\xa2\x9a\xab\xa2\x14\xd1\x01\x87yh\x979\xdc>\xb6\x85\xd0\xaa\x81\xa0\xe9FU\x8e(Y\x19\xb9Y\xa1\r\x85\x98\x18\xe3\x8bUm\x16d\x92\x8b\xbaSN\xed8\xa6\x92t\x99\xd3\xb3\xa4\x99$\xce\x92I\x99\xdd$\xa2\x92I\x92I$\x92d\x93$\x99\x92\xd6\x92\x93:m\x9fL\x07\'\x9d\xc3\x93\xa6S\xbaw\xd9mP;\xa0\xd2&\xb9\x17\xd0\xd9P\x97\xe9\x1f$\xd2Qh\x86\x08\xd3 \x8b,\xbavI\xec{HO*\xd9\xdd\xdep\x99\x84\x16q\x05\xdf\'t\xa3\x1a\xe9\xa4j\x07\xaec\x0fM0Q\x80\xf5P=C\x1d\xac]Z\x00\x8b\r\xedk3G\xa2\xab+V\xc4z\x86\xc9\xcf\xcd\xcc\x12\xb00\xb2\xf3\x86\x855F,\xd1L\x92\x93I\xdeI&\x93\'N\x93$\x92I\x9d\x92gI$\x99\xd2J)$\x99$\x92I$\x99%\x17I-\xb6\x8bJmG\xa7\xfb\x16f7\x19\xc4\x9f\x81\xd0\xe6f\xa9\xb9V\xdf\x01\xcb\xd9\xd9\xd5\xd2\xc7\xe9\xf6)\x18=\x1d\t<f\xee\xce\xec\x1emW\xd8\xad\xb2\xd2\xae\x93\xa7gx\xdb+%\x19E\x98\xe3.4\xab\x88\xb6\xc7M\\+\x84+\x1cQ\xd5\x03\xd5\x1a\xea\x1ecJ\x14\x07\x8f\x7fY\xa9$%\x0b4\x8e\xe6\xec,\xa8(\xd7tc^~VmY\xa1\xd1\x97\x9e\x1ept\xd3T#\x16d\xc9$\xf2SN\x93:t\xee\x92fI\x9d\x99&I;$\x93:J)2I$\x92I$\x92I\x93$\x97r\x15\row\xca\xf3~\xd5\xebY\x1c\x86\x1fa\xa5\x12r|c\x97\x9c\xa7e\xb2"\xc2\xf5\xbb\xfd\xda\x8d\x8e0e\x9e\\kR\xb2jJ1\x14\n\xa5e\xc4\xdcM\xaf(\xb3&I\xec\x9c"\xca\xd2.0\xa3o\xbeW\xd9:\xa1]pj\xe8\xaa\x9a\x07\x1e\xba\xe1\x85\xe4\x1e\xb1|I$l\xfc\xae\xaf\xa5uh\xe2\x89\x99\xbb\xd1\r\xcf\x83L\xa9\x8d1\xac,>Vl-`\x8f\x01\x85\x12\x88B\x0c\xd1d\xc9\xd3\xcd\xe4\xe9\xe2\x99II\xd9\xe4\xc94Tb\xc92N\x99$\x92d\x99&I$\x92I$\x92L\x99\'x\xfaeU\xf5\xe4iey\x17\xd0}\xd59\xba\x85\tQa\xf8\x87\x9f\xdb\'\xbawlJ\xbfN\xd80\xd1\xb0\x83r\xf4nv\x9cd\xf3f\x8d\xadFmNIgM\xd9\x92\x8afgh(\xc6V\x97u\xe5\xdfaR&\xe2\x1a\xba\xebh\xd7MC\x8fH\xd5@_\x15\xe4}oyVn\x95Y&u\xc5\x8f}u\xbeuZd\xe6\xe3\xd4\xf4a\x82<3G\xe6\xf3$\xd3\xb65@p\xe9\x84 \xcc\xcc\xc9\'y\xba\x92vL\x9d;\xbb\xbb3\xb3(\xc2,\x93\'d\x99\xd9:fL\x92I3\xa4\xce\xc9\xd9&I\'t\xde\xd3\x07\xe9\xf5\xe1\xa5\xc2t]\xc5\xd4B\xd8\x0c^?\x81a\xce\xd7v\xb3X\xbd\x0fe\x0c\x1b*\xc7\x94\xef \xc2\xa4\x9a\nr\x83\xd8\xee6h\xc5k\x12\xd1\x82\x82d\xef[E\x99\x99L\x83.\xb4\x82\xad\x9c\xae*u\xc6j\x88SH\xe3S\x06\xce\xf9\xf3\x1fS_\xb2\xd0\x91\xe7\\\xeb\xa265@\x93\xee\x10&\xaf\x0cQ\xa1\x89\xcf\xe2\x0f\x8fUy\xf1\x95\x96J0\xaa\x8ac\x18\xc5\x99$\x9d\xd4\xb4:\xa1\xf59\\ft\x94\x9aI&x\xa5\x18\xd6\xcc\x99;$\x932\x92\x8aL\x99\xd3:d\xd2\x8avI$\x92t\xde\xf2\x95\x9bz[\xbc\xe5\x1b\xd6\x0eE\xe9\x12/#\xe6\x98INfGc\xb7\xec\xea\xc6\x0e\xaan\x9c\xca8\xbb\x1d\xa9\xb1\xd4\x90\xd7\xbd\x80g\x9au\xb1\x8c!\x16vw\x8c\x1a,\xec\xa7u\xa4\x95i$J\xcb%4\xef*\xe9\xaa\xbaG\xa1Q\xe1\xdc\x8d\xddNF\xe7DN\xbd\xf5Xv\x96\xa9\x95N\xe7 q\x14\xf3\xb23\xf1a\x97\xca\xe2e\x87tYI\xddF\xb8V\xd1\x8afI;MG\xbe\xf5\xad\x07\xcb\xf2>"N\xcbe\xab\xccI\xd32hW\x14\xc9\x9d\xd9&L\xec\xec\x99$\x92gI\x9e.\x99$\x92I\'\xf7[m\x0fS\xa9\xdc\xce\xe66\x0e\x90\xc6^\xe5\x13\x9f\xcf\xf9^ 0\xd4\xd6[\xba\xdbQ\x16\x8a\xa0D\xe4QE\\\xa2\xd3\x15\xef\x90\xd2\xba\xd8\x8d)$\xd0\xae\t;\xb34\x19$\xf3"\xdbJ\xbc\x9b,\xb2\xe7\xb2\xf6Q\xa2\rD(\xa0_=\xf1\xcdZ\xe1\xbc\x07I\xa9\xb0R\xb0\x8d\x1d\xfd\t\xd98WIb_\x0c|no\r\xf1\xb0\x01\x01\x99\xd9$\xa3\x08\xc1\x93$\x92I%\x0e\xa7\xdb\xba"k\xf3O?\xdb\xcd\xe2u}\x7f%\xb8a1S\xc52hV\xcc\x93;\'L\xce\x93$\x93$\x92L\xe9&d\x92I\xd3\'\xf6\x99\xda\x8d\xdc\xec\xb3\xc5\xd6r\x96e\xc5Z\xf4er\x98\xdc\xbf-\xb5\xab\xad\xd0\xa9\xc1J\x98\xdd9\xdbu\xc45\x8f\x1a\xda3\x93\xa9\xa6x2\x8dqfg\x8bE33\xba\xb2\xe2o\xbe\xeb\xef\xba\xc9\xa9^\xee\xa3\n\xa8\xac|\x9f\x1e\xe2\xba\x8cm@w\xb9\xe2\xf4w\x88(\x9b\xf5\xb7\xb6\xae\xb6c\xd6\xdb5\xd5\x95\x0c\xfeg\'\'\'\x95\x06\xa8FJ)3F1d\xa4\xcf\x17I3\xc7\xae\xf4^\xd8\xfa\xbc\xf7\x7f\xb2\xaf\xc8\xfa>\xc3\x9e\r\xc5\xf3^1\x9e,\x99=u\xc5\x93\xa6t\xc9;2I$\x92d\x92gd\x92I$\x92\xef\xaem\x9d\xf2\xb4'"
[LINE:50]# INFO     [2021-04-05 15:11:48,424]  Asteptam mesaje...
.......
```
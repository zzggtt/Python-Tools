# -*- coding:utf-8 -*-
import argparse
import json
import socket
import sys
import ipaddr

def parse_args():
    parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' + sys.argv[0] + " -u http://www.baidu.com -d dir.txt")
    parser.add_argument("-i", "--ip", help="The ip address")
    parser.add_argument("-p", "--port", help="The port")
    return parser.parse_args()

def portscan(ip, port):
    s = socket.socket()
    try:
        s.connect((ip,port))
    except:
        res = None
        s.close()
    else:
        res = f'{ip + port} is alive'
    return res

def main(ip, port):
    result = portscan(ip, port)
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(result, ensure_ascii=False) + '\n')
        f.close()

if __name__ == '__main__':
    args = parse_args()
    ip = args.ip
    print(ip)
    ports = args.port.split(',')
    ips = ipaddr.IPNetwork(ip)
    for i in ips:
        for p in ports:
            main(str(i),int(p))

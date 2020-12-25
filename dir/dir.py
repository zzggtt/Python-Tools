# -*- coding:utf-8 -*-
import json
import sys,argparse
import requests

def parse_args():
    parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' + sys.argv[0] + " -u http://www.baidu.com -d dir.txt")
    parser.add_argument("-u", "--url", help="The website")
    parser.add_argument("-d", "--dir", help="The dir")
    return parser.parse_args()

def dirsearch(url, dir):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36"
    }
    try:
        response = requests.get(url=url+dir, headers=headers, timeout=3, verify=False)
    except requests.RequestException as err:
        status = None
        print(f'error:{err}')
    else:
        response.encoding = 'utf-8'
        status = response.status_code
    return status

def is_active(status ,url, dir):
    if status == 200:
        result = f'{url + dir} status coed is:200'
    else:
        result = f'{url + dir} not found'
    return result

def main(url, dir):
    code = dirsearch(url, dir)
    res = is_active(code, url, dir)
    print(res)
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(res, ensure_ascii=False) + '\n')
        f.close()

if __name__ == '__main__':
    args = parse_args()
    url = args.url
    dir = args.dir
    file_dir = open(dir,'r',encoding='utf-8')
    for file in file_dir:
        file = file.strip()
        main(url,file)


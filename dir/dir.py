# -*- coding:utf-8 -*-

import requests
import re,json,sys,argparse
from urllib.parse import urljoin

def parse_args():
    parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' + sys.argv[0] + " -u http://www.baidu.com")
    parser.add_argument("-u", "--url", help="The website")
    parser.add_argument("-f", "--file", help="The file contains url or js")
    return parser.parse_args()

# 爬取目标网页源码：
def request_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=3, verify=False)
    except requests.RequestException as err:
        html = None
        print(f'请求错误:{err}')
    else:
        response.encoding = 'utf-8'
        html = response.text
    return html

def extract_links(url,html):
    link_re = re.compile(r'<a[^>]+href\s*=\s*["\']([^"\']+)["\'][^>]*>', re.I)
    links = link_re.findall(html)
    return {urljoin(url, link) for link in links}

def write_links_to_file(link):
   print('find ===> ' + str(link))
   with open('links.txt', 'a', encoding='UTF-8') as f:
       f.write(json.dumps(link, ensure_ascii=False) + '\n')
       f.close()

def find_url(url):
    html = request_url(url)
    all_links = extract_links(url,html)
    for link in all_links:
        write_links_to_file(link)

if __name__ == '__main__':
    args = parse_args()
    url = args.url
    find_url(url)


### 目录扫描工具

设计思路很简单，只为了锻炼一下python：

![image-20201225150418576](C:\Users\80785\AppData\Roaming\Typora\typora-user-images\image-20201225150418576.png)



#### 0x01  模拟请求

函数功能分析：通过爬虫模拟请求，需要参数：url 、dir，返回状态码。

```python
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
```



#### 0x02 判断目录是否存在

这里很简单不做叙述：

```python
def is_active(status ,url, dir):
    if status == 200:
        result = f'{url + dir} status coed is:200'
    else:
        result = f'{url + dir} not found'
    return result
```



#### 0x03 结果保存

整合前面两个函数，并保存结果：

```python
def main(url, dir):
    code = dirsearch(url, dir)
    res = is_active(code, url, dir)
    print(res)
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(res, ensure_ascii=False) + '\n')
        f.close()
```



#### 0x04 获取命令行参数 

通过python的argparse库来获取命令行参数：

```python
def parse_args():
    parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' + sys.argv[0] + " -u http://www.baidu.com -d dir.txt")
    parser.add_argument("-u", "--url", help="The website")
    parser.add_argument("-d", "--dir", help="The dir")
    return parser.parse_args()
```

主函数处对获取到的文件需要做处理，因为从文件中获取到的数据，每一行后又\n，这里通过strip()函数进行处理：

```pytho
if __name__ == '__main__':
    args = parse_args()
    url = args.url
    dir = args.dir
    file_dir = open(dir,'r',encoding='utf-8')
    for file in file_dir:
        file = file.strip()
        main(url,file)
```


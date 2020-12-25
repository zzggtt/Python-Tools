### 端口扫描

端口扫描主要用于练习sockets通信，这里简单的根据状态码来判断端口是否存活。



#### 0x01 sockets通信

python通过导入socket模块，就能完成sockets通信，主要流程很简单，如下：

```python
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
```



#### 0x02 保存数据

保存数据已经很熟悉了，直接贴代码：

```python
def main(ip, port):
    result = portscan(ip, port)
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(result, ensure_ascii=False) + '\n')
        f.close()
```



#### 0x03 输入

输入的参数主要有两个：ip和端口。

ip既要考虑单个ip的处理，又要考虑c段、b段等处理，这里采用导入ipaddr模块来完成：

```python
ipaddr.IPNetwork(ip)
```

然后端口的获取要解决字符串分割成数组的形式：

```python
args.port.split(',')
```

整个逻辑如下：

```python
if __name__ == '__main__':
    args = parse_args()
    ip = args.ip
    print(ip)
    ports = args.port.split(',')
    ips = ipaddr.IPNetwork(ip)
    for i in ips:
        for p in ports:
            main(str(i),int(p))
```










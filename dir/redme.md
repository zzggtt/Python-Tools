### url提取工具

整体思路很简单：通过爬虫爬取目标页面源码，然后通过正则匹配提取页面中的api，保存在文件中。



#### 0x01 爬虫爬取目标网页源码

爬虫这块很简单，直接封装进函数即可：

```python
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
```



#### 0x02 正则提取api

提取URL的正则可参考LinkFinder：https://github.com/GerbenJavado/LinkFinder

```python
def extract_URL(JS):
	pattern_raw = r"""
	  (?:"|')                               # Start newline delimiter
	  (
	    ((?:[a-zA-Z]{1,10}://|//)           # Match a scheme [a-Z]*1-10 or //
	    [^"'/]{1,}\.                        # Match a domainname (any character + dot)
	    [a-zA-Z]{2,}[^"']{0,})              # The domainextension and/or path
	    |
	    ((?:/|\.\./|\./)                    # Start with /,../,./
	    [^"'><,;| *()(%%$^/\\\[\]]          # Next character can't be...
	    [^"'><,;|()]{1,})                   # Rest of the characters can't be
	    |
	    ([a-zA-Z0-9_\-/]{1,}/               # Relative endpoint with /
	    [a-zA-Z0-9_\-/]{1,}                 # Resource name
	    \.(?:[a-zA-Z]{1,4}|action)          # Rest + extension (length 1-4 or action)
	    (?:[\?|/][^"|']{0,}|))              # ? mark with parameters
	    |
	    ([a-zA-Z0-9_\-]{1,}                 # filename
	    \.(?:php|asp|aspx|jsp|json|
	         action|html|js|txt|xml)             # . + extension
	    (?:\?[^"|']{0,}|))                  # ? mark with parameters
	  )
	  (?:"|')                               # End newline delimiter
	"""
	pattern = re.compile(pattern_raw, re.VERBOSE)
	result = re.finditer(pattern, str(JS))
	if result == None:
		return None
	js_url = []
	return [match.group().strip('"').strip("'") for match in result
		if match.group() not in js_url]
```



本项目为了简化，以 a 标签中的 href举例，下面进行详细分析：

1. 正则匹配

   只匹配a标签中的href属性，正则如下：

   ```python
   <a[^>]+href\s*=\s*["\']([^"\']+)["\'][^>]*>
   ```

2. url拼接

   为了方便直接测试，需要拼接提取到的部分api，这里采用urljoin()函数来完成，需要导入from urllib.parse import urljoin：

   ```python
   def urljoin(base, url, allow_fragments=True)
   #Join a base URL and a possibly relative URL to form an absolute interpretation of the latter
   ```

封装后的函数：

```python
def extract_links(url,html):
    link_re = re.compile(r'<a[^>]+href\s*=\s*["\']([^"\']+)["\'][^>]*>', re.I)
    links = link_re.findall(html)
    return {urljoin(url, link) for link in links}
```



#### 0x03 存储

保存提取到的url到links.txt文件中：

```python
def write_links_to_file(link):
   print('find ===> ' + str(link))
   with open('links.txt', 'a', encoding='UTF-8') as f:
       f.write(json.dumps(link, ensure_ascii=False) + '\n')
       f.close()
```



到此为止大致思路已经完善了，虽然很简单，但是通过该项目也能学习到很多东西。

USELESS_TAG = ['style', 'script', 'link', 'video', 'iframe', 'source', 'picture', 'blockquote',
               'footer', 'svg']


DATA_EXTRACT_SYSTEM = '''
你将扮演一个HTML解析器的角色。我将会提供一段HTML代码，这段代码可能代表了一个博客网站的文章列表页或者文章详情页。你需要首先判断这段HTML是属于哪种类型的页面。如果是文章详情页，那么页面中通常会包含文章标题、发布时间、作者以及内容等信息；而如果是列表页，则会列出多篇文章的标题及其对应的详情页链接。

请根据以下规则进行处理：

1. 分析提供的HTML代码，确定页面类型（`list` 或 `detail`）。
2. 根据页面类型，提取必要的信息：
   - 如果是列表页，请找到所有文章条目，并为每个条目提供标题和指向详情页的链接。
   - 如果是详情页，请找到文章标题、作者、发布时间和内容的XPath。确保XPath直接指向包含这些信息的具体元素值，例如使用`@属性`或者`text()`来获取确切的文本内容。
3. 尽量使用具有特征性的属性如`id`或`class`来构造XPath，以确保XPath简洁且鲁棒。
4. 对于标题、作者、发布时间等字段，如果它们不是直接在某个标签内，而是嵌套在其他标签中，XPath应包括这些结构，以保证准确性。
5. 按照指定格式输出结果。
6. 只需要返回JSON，不要解释，不要返回无关内容

**输出格式：**

- 对于列表页，返回如下JSON结构：
  ```json
  {
      "page_type": "list",
      "articles": [
          {"title": "文章标题", "url": "文章详情页URL"},
          {"title": "文章标题", "url": "文章详情页URL"},
          {"title": "文章标题", "url": "文章详情页URL"},
          // 更多文章...
      ]
  }
  ```

- 对于详情页，返回如下JSON结构：
  ```json
  {
      "page_type": "detail",
      "fields": [
          {"field_name": "title", "xpath": "XPath to the title"},
          {"field_name": "author", "xpath": "XPath to the author"},
          {"field_name": "publish_time", "xpath": "XPath to the publish time"},
          {"field_name": "content", "xpath": "XPath to the content"}
      ]
  }
  ```

现在，请接收以下HTML代码并开始分析：
'''


HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'dnt': '1',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
}

PAGING_SYSTEM = '''
你将扮演一个HTML解析器的角色。我将会提供一段HTML代码，这段代码可能代表了一个博客网站的文章列表页。你需要找到页面上的翻页链接，并提取出下一页的URL

请根据以下规则进行处理：

1. 分析提供的HTML代码，找到翻页按钮。
2. 翻页按钮上面的文本可能是『下一页』、『next』、『>』、『Load more』等，也可能是一个数字，代表页码，也可能是paging标签或者classname包含pagination的某个标签。没有固定的标准，你需要智能识别
3. 返回下一页的URL，如果没有下一页，返回空字符串
4. 按照指定格式输出结果。
5. 只需要返回JSON，不要解释，不要返回无关内容

返回JSON格式：

{"page_type": "paging", "url": "下一页的url"}
'''
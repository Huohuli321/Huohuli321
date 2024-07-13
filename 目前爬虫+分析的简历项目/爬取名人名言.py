from bs4 import BeautifulSoup
import requests
import csv

# 定义网站的URL
url = 'http://quotes.toscrape.com'

# 获取html文件并使用html.parser进行解析
# 使用 requests.get(url) 发送请求到目标网站。
# html 变量存储了响应的文本内容。
html = requests.get(url)

# bs 变量是 Beautiful Soup 对象，用于解析 html 变量中的 HTML 内容。
soup = BeautifulSoup(html.text, 'html.parser')

try:

    # 使用 open('quote_list.csv', 'w') 尝试创建或打开一个名为 "quote_list.csv" 的文件用于写入。
    # csv_file是文件对象。
    # csv_file 在这段代码中是 CSV 文件对象的引用，用于管理和操作 CSV 文件的读写操作。
    csv_file = open('quote_list.csv', 'w',)

    # 定义 “名言内容”、“作者”、“标签”
    fieldnames = ['quote', 'author', 'tags']
    """
      csv.DictWriter: 这是 csv 模块中的一个类，用于创建一个写入器对象，该对象可以将字典数据写入 CSV 文件。
      csv_file: 这是一个文件对象，通常是通过 open 函数创建的，用于表示要写入的 CSV 文件。在这个上下文中，
      csv_file 应该是之前通过 open('quote_list.csv', 'w') 创建的文件对象。
      ieldnames=fieldnames: 这是一个关键字参数，它接收一个字符串列表 fieldnames，该列表定义了 CSV 文件的列名。
      这些列名将作为 CSV 文件的标题行写入，并且在之后写入的每一行数据中，这些列名将对应字典中的键。
    """
    dictwriter = csv.DictWriter(csv_file, fieldnames=fieldnames)

    """
      dictwriter.writeheader() 是 Python csv 模块中 DictWriter 类的一个方法，
      用于将定义好的列标题（字段名）写入到 CSV 文件的开头作为标题行。这个方法在开始写入数据之前调用一次，以创建 CSV 文件的结构。
      当你使用 csv.DictWriter 类创建一个对象时，你提供了一个字段名列表（fieldnames），
      这个列表定义了 CSV 文件中的列标题。writeheader() 方法会将这些字段名写入文件，每个字段名之间用逗号分隔，并在第一行结束。
      csv文件标题行。
    """
    dictwriter.writeheader()

    # while True 创建一个无限循环，直到找到下一页的链接为止。
    while True:

        # 遍历页面上所有的名言，使用 bs.findAll('div', {'class': 'quote'}) 查找div标签下所有类名为 "quote" 的 <div> 元素。
        # 使用 find_all 方法查找所有 class 为 'quote' 的 div 标签
        for quote in soup.findAll('div', {'class': 'quote'}):

            # 提取名言内容、作者和标签的文本部分

            # 这个方法在 quote 元素内查找第一个匹配的子元素，条件是该子元素的标签名是 <span> 且其 class 属性等于 'text'。
            # 这是一个查找操作，返回找到的第一个匹配的 Tag 对象。
            # .text: 这是一个属性，它获取 Tag(标签) 对象中的文本内容。
            # 如果 find 方法成功找到了一个 <span> 标签，.text 将会提取这个标签内的纯文本内容。
            text = quote.find('span', {'class': 'text'}).text
            # 和以上代码行类似
            author = quote.find('small', {'class': 'author'}).text
            # 定义一个空列表，作用是存储从 HTML 文档中提取的标签。
            tags = []
            for tag in quote.findAll('a', {'class': 'tag'}):
                # 用于将 tag 对象的 text 属性添加到名为 tags 的列表中。
                tags.append(tag.text)
            # 将当前的名言内容、作者和标签写入csv文件
            # dictwriter.writerow 是 Python csv 模块中 DictWriter 类的一个方法，writerow() 方法将一个包含数据的列表写入到CSV文件中。
            # 这个方法接受一个字典作为参数，字典的键应该与 DictWriter 对象初始化时指定的字段名相匹配。
            dictwriter.writerow({'quote': text, 'author': author, 'tags': tags})

        # 查找到下一页的链接
        next = soup.find('li', {'class': 'next'})

        # 这两行代码的目的是检查当前页面是否还有下一页。
        # 如果 next 变量是 None，说明没有找到表示“下一页”的元素，因此爬虫达到了最后一页，循环应该被终止。如果 next 变量不是 None，则循环会继续，
        if not next:
            break
        """
          下面两行代码，获取并解析下一页的html文件。
          
         1. 从 next 变量中的 <a> 标签获取 href 属性，这通常是下一页的 URL。
         2.将这个 URL 与基础 URL（url）拼接起来，形成一个完整的 URL。
         3. 使用 requests.get 发送一个 GET 请求到这个完整的 URL。这种技术允许爬虫自动从一个页面移动到下一个页面，直到遍历完所有页面或者满足某个停止条件。
         4. 加号 + 被用来拼接两个字符串：url 变量和 next.a.attrs['href'] 变量的值。
            这种拼接是因为您需要将基础 URL（url）和页面的相对链接（next.a.attrs['href']）组合成一个完整的 URL，
            以便 requests.get 函数可以正确地向这个完整的 URL 发送请求。
        """
        # next.a.attrs['href'] 就是在访问 next 变量中的 <a> 标签对象的 attrs 字典，并获取 href 属性的值。这个值通常是一个 URL，可以用于发送 HTTP 请求到下一个页面。
        # a.attrs意思是：访问 <a> 标签的所有属性，输出将会是一个字典，包含了 href、class 和 id 属性。
        # a.attrs['href']只包含了href属性。
        html = requests.get(url + next.a.attrs['href'])
        bs = BeautifulSoup(html.text, 'html.parser')
except:
    # 未知错误
    print('Unknown Error!!!')
finally:
    # 关闭文件对象
    csv_file.close()
from selenium import webdriver
import requests     #使用 requests 提供的方法.get向指定 URL(网址) 发送 HTTP 请求到指定url
import os
from bs4 import BeautifulSoup  #BeautifulSoup是一个第三方python库，用于从HTML或XML文档中提取数据
import time

# path= E:\web scraping\chromedriver_win32\chromedriver.exe 设置ChromeDriver的路径。
# path = input("Enter Path : ") 输入获取ChromeDriver的路径（浏览器驱动的路径）

url = input('请输入要爬取的网站地址:')  #需要爬取的网站url

output = "output"  #用作目录


def get_url(url):
    # 这行代码初始化了一个Chrome WebDriver的实例，并将其赋值给变量driver。
    # WebDriver是Selenium库中的一个组件，它允许您自动化和控制一个Web浏览器实例。
    driver = webdriver.Chrome()
    # driver.get(url) 方法用于导航到指定的URL，但它并不返回网页的内容或其加载状态。这个方法没有返回值（或者说它的返回值是None）
    driver.get(url)
    print("loading.....")
    """
    driver.execute_script()：Selenium WebDriver的方法，用于执行JavaScript代码。
    document.documentElement.outerHTML:
        1.document：代表当前加载的网页的DOM（文档对象模型）。
        2.documentElement：是document对象的一个属性，它返回文档的根元素。对于HTML文档，这通常是<html>标签。
        3.outerHTML：是一个属性，返回描述元素及其内容的序列化HTML片段。
    当你使用driver.execute_script("return document.documentElement.outerHTML")时，你实际上是在执行一段JavaScript代码，
    这段代码通过document.documentElement获取到了当前文档的根元素（即<html>标签,
    然后通过.outerHTML属性获取到了这个根元素及其内部所有内容的HTML字符串。
    这个字符串就是当前页面的完整HTML内容，包括所有的HTML标签、属性和文本内容。
    """
    res = driver.execute_script("return document.documentElement.outerHTML")
    return res


def get_img_links(res):
    soup = BeautifulSoup(res, "lxml")  #beautifulsoup(解析内容：res,解析器："lxml")，soup是解析之后的解析对象。

    """
    在Python的BeautifulSoup库中，find_all()方法用于查找文档中所有符合指定条件的标签。
    当你使用find_all("img", src=True)时，你正在寻找所有<img>标签，并且这些标签必须有一个src属性。
        1.img：这是你希望查找的标签名称，即<img>标签。
        2.src=True：这是一个过滤器，它告诉BeautifulSoup只返回那些具有src属性的<img>标签。
        具体来说，src=True是一个简写形式，等同于一个更复杂的过滤器，如{"src": True}。
        但是，实际上，这个过滤器并不检查src属性的值是否为True（因为属性的值通常是字符串，而不是布尔值）。
        相反，它只是确保<img>标签有一个src属性。
    """
    # imglinks里面保存了标签对应的图片的URL
    imglinks = soup.find_all("img", src=True)
    return imglinks


def download_img(img_link, index):
    try:
        extensions = [".jpeg", ".jpg", ".png", ".gif"]
        extension = ".jpg"
        for exe in extensions:
            # 这检查img_link中是否包含当前循环中的扩展名exe
            if img_link.find(exe) > 0:
                extension = exe
                break
        """"
        rq.get(img_link) 会发起请求并返回一个 Response 对象，其中包含了服务器的响应信息。
        .content 是 Response 对象的一个属性，它包含了原始的二进制响应数据。在这个上下文中，
        img_data 将存储图片的二进制数据。
        这是因为图片文件（如 JPEG、PNG 等）是二进制格式的，而不是文本格式。
        requests.get(img_link).content 这行代码的目的是发送一个 HTTP GET 请求到指定的图片链接，并获取返回的二进制图片数据。
        """
        img_data = requests.get(img_link).content
        """
        output包含文件保存的路径。\\是Windows系统中的路径分隔符。str(index + 1)将index加1并转换为字符串，用于给文件命名。
        extension是前面确定的图片文件的扩展名。
        "wb+"表示以二进制格式打开文件用于读写
        """
        with open(output + "\\" + str(index + 1) + extension, "wb+") as f:
            f.write(img_data)

        f.close()
    except Exception:
        pass

# result里存放的是，它会返回整个页面的 HTML 源码作为字符串（前端HTML代码）
result = get_url(url)
# 程序延时30秒
time.sleep(30)
# img_links里面保存了标签对应的图片的URL
img_links = get_img_links(result)
"""
以下两条代码用于检查 output 指定的路径是不是一个不存在的目录。如果不存在则创建目录
os.path.isdir(path) 是 Python 的 os.path 模块中的一个函数，用于检查一个路径（path）是否对应一个存在的目录。
如果路径存在且是一个目录，它返回 True；否则，它返回 False。 path：一个字符串，表示要检查的路径。
"""
if not os.path.isdir(output):
    """
    os.mkdir(path) 是一个函数，用于在指定的 path 创建一个新的目录。如果 path 已经存在，这个函数会抛出一个 FileExistsError 异常。
    output是一个变量，它应该包含一个字符串，这个字符串表示你想要创建的目录的路径。
    这个路径可以是绝对路径（例如，/home/user/new_directory），也可以是相对于当前工作目录的相对路径（例如，new_directory）。
    """
    os.mkdir(output)

# enumerate(iteration, start)函数默认包含两个参数，其中iteration参数为需要遍历的参数，比如字典、列表、元组等，
# start参数为开始的参数，默认为0（不写start那就是从0开始）。
# enumerate函数有两个返回值，第一个返回值为从start参数开始的数，第二个参数为iteration参数中的值
# index中保存的是与img_link2数据的索引，img_link2保存的是数据(图片URL地址)
for index, img_link2 in enumerate(img_links):
    """
    这行代码从当前字典img_link2中获取 "src" "键"对应的"值"，并将这个值存储在变量 iml_url 中。这个值通常是一个图片的 URL。
    这里我们像操作字典一样访问img_link2标签的src属性,但实际上，img_link2是一个Tag对象，不是字典。
    如果你从BeautifulSoup的find_all()方法获取了一个列表，其中每个元素看起来像HTML代码，但实际上它们是BeautifulSoup的Tag对象。这些对象在大多数情况下可以被当作字典来操作，因为它们提供了类似字典的访问方式来获取标签的属性。
    例如，当你使用soup.find_all("img", src=True)时，你得到的是一个包含所有<img>标签的列表，这些标签都有src属性。你可以像操作字典一样，使用[]操作符来获取这些标签的src属性。
    但是，这些元素并不是真正的字典；它们是BeautifulSoup的Tag对象。只是当你尝试通过标签名称（比如src）访问它们时，BeautifulSoup会尝试返回相应的属性值，这使得它们看起来像字典。
    """
    img_url = img_link2["src"]
    print("Downloading...")
    if img_url:
        download_img(img_url, index)
print("Download Complete!!")
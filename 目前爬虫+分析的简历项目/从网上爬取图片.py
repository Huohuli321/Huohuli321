import requests
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import os
# 图片url在HTML代码中基本上都是img标签对应的src属性。例如：<img src="http://example.com/image.jpg" alt="示例图片">
# alt 属性是 <img> 标签的另一个常用属性，它提供了图片的替代文本，当图片无法显示时，它会显示给用户。

# url = 'https://dribbble.com/'
# 用户输入网址
url = input("请输入你要爬取的网址：")
# 创建个字符串用来创建目录
output = "output"
def get_url(url):
    # 创造谷歌浏览器对象
    driver = webdriver.Chrome()
    # driver.get(url)的作用是让 WebDriver 打开一个浏览器窗口，并导航到指定的 URL
    driver.get(url)
    print("加载中.....")
    # 通过execute_script执行JAVAscript代码，返回整张页面元素
    res = driver.execute_script("return document.documentElement.outerHTML")
    return res
def get_img_links(res):
    # 对整个页面的HTML代码进行解析
    soup = BeautifulSoup(res, 'lxml')
    # 网站代码层级变了，但是使用find_all依然能获取到。获取所有标签名为img的src属性
    imglinks = soup.find_all('img', src=True)
    return imglinks
def download_iml(index, data_url):
    try:
        # 定义图片扩展名的列表
        extensions = ['.jpeg', '.jpg', '.png', '.gif']
        extension = '.jpg'
        # 遍历列表
        for exe in extensions:
            # endswith 方法只关注字符串的最后一部分，也就是文件的扩展名部分，而忽略 ?resize=400x0 这类查询参数。
            # 它主要是判断字符串是否以指定的文件扩展名（如 .jpg、.png 等）结束，而不管扩展名之前是否有其他的额外字符，只要最后的扩展名部分匹配就会返回 True 。
            # endswith()方法:用于检查一个字符串是否以指定的后缀（字符串）结尾。
            if data_url.endswith(exe):
                extension = exe
                break
        # 对图片URL发起请求；.content 属性获取的是响应的原始二进制内容
        img_data = requests.get(data_url).content
        # 打开文件
        with open(output + "\\" + str(index + 1) + extension, "wb+") as f:
            # 写入文件
            f.write(img_data)
    # 捕获所有异常
    # 表示捕获所有类型的异常，并将捕获到的异常对象赋值给变量 e
    except Exception as e:
        # 这一行则是在捕获到异常后，打印出一条提示信息，告知用户发生了异常，并将异常对象的相关信息（通常是异常的描述）输出，以便于了解异常的具体情况。
        # 例如，如果在 try 代码块中发生了除零错误，那么输出可能是 发生了异常: division by zero 。
        print("发生了异常:", e)

# 主要执行代码：
# 对输入的URL发起请求(使用get_url函数)
result = get_url(url)
time.sleep(30)
# 获取带有图片地址的HTML代码
img_links = get_img_links(result)
# 判断目录是否存在
if not os.path.isdir(output):
    # 不存在则创造相对路径的目录
    os.mkdir(output)
# 遍历获取带有图片地址的HTML代码
for index, img_dict in enumerate(img_links):
     # 将图片地址抽取出来赋值
     iml_url = img_dict["src"]
     print("下载中....")
     # 如果图片地址不为空
     if iml_url:
         # 对图片URL进行处理
         download_iml(index, iml_url)
print("下载完成!!!")

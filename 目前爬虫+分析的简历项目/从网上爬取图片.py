import requests
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import os
# 图片url在HTML代码中基本上都是img标签对应的src属性。例如：<img src="http://example.com/image.jpg" alt="示例图片">
# alt 属性是 <img> 标签的另一个常用属性，它提供了图片的替代文本，当图片无法显示时，它会显示给用户。

# url = 'https://dribbble.com/'
url = input("请输入你要爬取的网址：")
output = "output"
def get_url(url):
    driver = webdriver.Chrome()
    # driver.get(url)的作用是让 WebDriver 打开一个浏览器窗口，并导航到指定的 URL
    driver.get(url)
    print("加载中.....")
    res = driver.execute_script("return document.documentElement.outerHTML")
    return res
def get_img_links(res):
    # 对整个页面的HTML代码进行解析
    soup = BeautifulSoup(res, 'lxml')
    imglinks = soup.find_all('img', src=True)
    return imglinks
def download_iml(index, data_url):
    try:
        extensions = ['.jpeg', '.jpg', '.png', '.gif']
        extension = '.jpg'
        for exe in extensions:
            if data_url.endswith(exe):
                extension = exe
                break
        img_data = requests.get(data_url).content
        with open(output + "\\" + str(index + 1) + extension, "wb+") as f:
            f.write(img_data)
    except Exception:
        pass

result = get_url(url)
time.sleep(30)
# 获取图片的URL地址
img_links = get_img_links(result)
if not os.path.isdir(output):
    # 创造相对路径的目录
    os.mkdir(output)
for index, img_dict in enumerate(img_links):
     iml_url = img_dict["src"]
     print("下载中....")
     if iml_url:
         download_iml(index, iml_url)
print("下载完成!!!")




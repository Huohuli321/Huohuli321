# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy
# class ZhanzhangtupianPipeline:
#     def process_item(self, item, spider):
#         return item

# 自定义管道类
class imgsPileLine(ImagesPipeline):

    # 这个方法可以对图片地址进行请求
    def get_media_requests(self, item, info):
        yield scrapy.Request(item['src'])

    # 指定图片存储的路径   request:上个发放请求发送返回的请求对象
    def file_path(self, request, response=None, info=None, *, item=None):
        imgName = request.url.split("/")[-1]
        return imgName
    """
        'item_completed 方法返回的项目（item）将被发送回 Scrapy 的项目处理流程中。这意味着，如果还有其他管道（pipeline）组件被启用，
        它们将按照在 ITEM_PIPELINES 设置中定义的顺序继续处理这个项目。如果没有其他管道组件，或者该项目已经到达管道链的末尾，
        那么项目将被丢弃，不再进行任何进一步的处理。'
        在您的代码中，item_completed 方法返回了项目 item，这意味着：
        1.如果有其他管道组件，项目将被传递给下一个管道组件的 process_item 方法。
        2.如果没有其他管道组件，或者该项目已经完成所有管道组件的处理，项目将被丢弃，不再进行任何操作。
    """
    # 目前这个项目不启用也能爬下来
    def item_completed(self, results, item, info):
          # item里面是图片地址
        return item  # 返回给下一个即将被执行的管道类




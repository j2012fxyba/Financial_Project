
import scrapy
# 运行爬虫并保存到 JSON 文件
#scrapy crawl books -o books.json

# 或者只运行爬虫 (数据将通过 pipelines 处理)
#scrapy crawl books


from scrapy import cmdline
cmdline.execute("scrapy crawl books -s LOG_ENABLED=False".split())
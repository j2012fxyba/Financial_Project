'''

使用正则表达式截取html文件里面的 <img src> 图片地址标签，并拼接完整的图片下载路径
使用sprider 爬取服务器图片到本地文件夹
'''



import os
import re
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup


# 示例HTML内容(也可以直接用requests获取网页)
html = """
    <html>
        <body>
            <img src="images/logo.png">
            <img data-src="https://example.com/pic.jpg" alt="示例">
            <img src="/static/photo.webp">
        </body>
    </html>
    """

def download_images_from_html(html_content, base_url, output_dir='images'):
    """
    从HTML中提取图片并下载到本地
    
    参数:
        html_content: HTML内容字符串
        base_url: 基准URL(用于合并相对路径)
        output_dir: 图片保存目录(默认'images')
    """
    # 创建保存目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 方法1: 使用正则表达式提取img src
    img_urls = set()
    #pattern：要编译的正则表达式字符串（通常使用原始字符串 r'' 避免转义问题）
    img_pattern = re.compile(r'<img[^>]+src=["\'](.*?)["\']', re.IGNORECASE)
    img_urls.update(img_pattern.findall(html_content))
    
    # 方法2: 用BeautifulSoup再提取一次(更可靠)
    soup = BeautifulSoup(html_content, 'html.parser')
    for img in soup.find_all('img'):
        if img.get('src'):
            img_urls.add(img['src'])
        if img.get('data-src'):  # 处理懒加载图片
            img_urls.add(img['data-src'])
    
    # 下载图片
    for i, img_url in enumerate(img_urls):
        try:
            # 合并相对路径为完整URL
            full_url = urljoin(base_url, img_url)
            
            # 获取图片内容
            response = requests.get(full_url, stream=True, timeout=10)
            response.raise_for_status()
            
            # 从URL提取文件名
            filename = os.path.basename(img_url.split('?')[0])  # 去除URL参数
            if not filename:  # 如果URL不以文件名结尾
                filename = f'image_{i}.jpg'
            
            # 补充文件扩展名
            if not os.path.splitext(filename)[1]:
                content_type = response.headers.get('content-type', '')
                if 'jpeg' in content_type or 'jpg' in content_type:
                    filename += '.jpg'
                elif 'png' in content_type:
                    filename += '.png'
                elif 'gif' in content_type:
                    filename += '.gif'
                else:
                    filename += '.bin'
            
            # 保存图片
            save_path = os.path.join(output_dir, filename)
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            
            print(f"下载成功: {full_url} -> {save_path}")
            
        except Exception as e:
            print(f"下载失败 {img_url}: {str(e)}")

# 使用示例
if __name__ == '__main__':
    
    
    # 基准URL(用于合并相对路径)
    base_url = "https://example.com"
    
    # 执行下载
    download_images_from_html(html, base_url)
import requests
import re
import json
import threading
import pymongo

def flush_data(data):
    if '肤' in data:
        return '肤色'
    if '黑' in data:
        return '黑色'
    if '紫' in data:
        return '紫色'
    if  '粉' in  data:
        return '粉色'
    if  '蓝' in  data:
        return '蓝色'
    if  '白' in  data:
        return '白色'
    if  '灰' in  data:
        return '灰色'
    if  '槟' in  data:
        return '香槟色'
    if  '琥' in  data:
        return '琥珀色'
    if  '红' in  data:
        return '红色'
    if  '紫' in  data:
        return '紫色'
    if  'A' in  data:
        return 'A'
    if  'B' in  data:
        return 'B'
    if  'C' in  data:
        return 'C'
    if  'D' in  data:
        return 'D'


def find_product_id(key_word):
    jd_url = 'https://search.jd.com/Search'
    product_ids = []
    #  爬前3页的商品
    for key_word in range(1,3):
        param = {'keyword': key_word, 'enc': 'utf-8', 'page': i}
        response = requests.get(jd_url,params=param)
        ids = re.findall('data-pid="(.*?)"', response.text, re.S)
        product_ids += ids
        return product_ids

"""获取评论内容"""

def get_comment_message(product_id):
    urls = ['https://sclub.jd.com/comment/productPageComments.action?'
            'callback=fetchJSON_comment98vv53282&' \
            'productId={}' \
            '&score=0&sortType=5&' \
            'page={}' \
            '&pageSize=10&isShadowSku=0&rid=0&fold=1'.format(product_id, page) for page in range(1, 11)]
    for url in urls:
        response = requests.get(url)
        html = response.text
        html = html.replace('fetchJSON_comment98vv53282(', '').replace(');', '')
        data = json.loads(html)
        comments = data['comments']
        t = threading.Thread(target=save_mongo, args=(comments,))
        t.start()


def save_mongo(comments):
    for comment in comments:
        product_data = {}
        product_data['product_color'] = flush_data(comment['productColor'])
        product_data['product_size'] = flush_data(comment['productSize'])
        product_data['comment_content'] = comment['content']
        product_data['create_time'] = comment['creationTime']
        # 插入mongo
        # flush_data清洗数据的方法
        product_db.insert(product_data)

lock = threading.Lock()

# 获取评论线程
def spider_jd(ids):
    while ids:
        # 加锁
        lock.acquire()
        # 取出第一个元素
        id = ids[0]
        # 将取出的元素从列表中删除，避免重复加载
        del ids[0]
        # 释放锁
        lock.release()
        # 获取评论内容
        get_comment_message(id)


product_ids = find_product_id('胸罩')
for i in (1, 5):
    # 增加一个获取评论的线程
    t = threading.Thread(target=spider_jd, args=(product_ids,))
    # 启动线程
    t.start()


if __name__ =="__main__":
    from pylab import *
    client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
    # jd数据库
    db = client.jd
    # product表,没有自动创建
    product_db = db.product
    # jd数据库
    db = client.jd
    # product表,没有自动创建
    product_db = db.product
    # 统计以下几个颜色
    color_arr = ['肤色', '黑色', '紫色', '粉色', '蓝色', '白色', '灰色', '香槟色', '红色']

    color_num_arr = []
    for i in color_arr:
        num = product_db.count({'product_color': i})
        color_num_arr.append(num)

    # 显示的颜色
    color_arr = ['bisque', 'black', 'purple', 'pink', 'blue', 'white', 'gray', 'peru', 'red']

    #labeldistance，文本的位置离远点有多远，1.1指1.1倍半径的位置
    #autopct，圆里面的文本格式，%3.1f%%表示小数有三位，整数有一位的浮点数
    #shadow，饼是否有阴影
    #startangle，起始角度，0，表示从0开始逆时针转，为第一块。一般选择从90度开始比较好看
    #pctdistance，百分比的text离圆心的距离
    #patches, l_texts, p_texts，为了得到饼图的返回值，p_texts饼图内部文本的，l_texts饼图外label的文本
    patches,l_text,p_text = plt.pie(sizes, labels=labels, colors=colors,
                                    labeldistance=1.1, autopct='%3.1f%%', shadow=False,
                                    startangle=90, pctdistance=0.6)
    #改变文本的大小
    #方法是把每一个text遍历。调用set_size方法设置它的属性
    for t in l_text:
        t.set_size=(30)
    for t in p_text:
        t.set_size=(20)
    # 设置x，y轴刻度一致，这样饼图才能是圆的
    plt.axis('equal')
    plt.title("内衣颜色比例图", fontproperties="SimHei") #
    plt.legend()
    plt.show()


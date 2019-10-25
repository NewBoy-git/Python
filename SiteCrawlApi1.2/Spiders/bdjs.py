from lxml import etree

import requests

def baidu_search(phone):
    url = 'http://www.baidu.com/s?wd={}'
#
#     r = requests.get(url.format(phone)).text
#     content = etree.HTML(r)
#     title = content.xpath("//h3[@class='t']/a/text()[1]")
#     href = content.xpath("//h3[@class='t']/a/@href")
    # print(title)
    # print(href)
    # print(len(href))
    # for ti in title:
    #     if len(ti)<3:
    #         title.remove(ti)
    # list = []
    # item_al ={}
    # print(len(title))
    # for i in range(2,len(title)):
    #     item = {}
    #     item['title'] = title[i]
    #     item['href'] = href[i]
    #     abstract = content.xpath("//div["+str(i)+"]/div[@class='c-abstract']/text()")
    #     item['abstract'] = ''.join(abstract)
    #     list.append(item)
    # print(list)
    # item_al['data'] = list
    # item_al['type'] = 'bdjs'
    # return item_al

# def baidu_search(phone):
#     url = 'http://www.baidu.com/s?wd={}'
#
#     r = requests.get(url.format(phone)).text
#     content = etree.HTML(r)
#     title = content.xpath("//h3[@class='t']/a/text()[1]")
#     href = content.xpath("//h3[@class='t']/a/@href")
#     # for ti in title:
#     #     if len(ti)<3:
#     #         title.remove(ti)
#     # if title > 10:
#     #     title = title[:10]
#     list = []
#     item_al ={}
#     print(len(title))
#     for i in range(2,len(title)):
#         item = {}
#         item['title'] = title[i]
#         item['href'] = href[i]
#         abstract = content.xpath("//div[@id="+str(i)+"]/div[@class='c-abstract']/text()")
#         item['content'] = ''.join(abstract)
#         list.append(item)
#     # print(list)
#     item_al['data'] = list
#     item_al['type'] = 'bdjs'
#     return item_al

    r = requests.get(url.format(phone)).text
    content = etree.HTML(r)
    title = content.xpath("//h3[@class='t']/a/text()[1]")
    href = content.xpath("//h3[@class='t']/a/@href")
    # for ti in title:
    #     if len(ti)<3:
    #         title.remove(ti)
    # if title > 10:
    #     title = title[:10]
    list = []
    item_al = {}
    print(len(title))
    for i in range(2, len(title) + 2):
        item = {}
        item['title'] = title[i - 2]
        item['href'] = href[i - 2]
        abstract = content.xpath("//div[" + str(i) + "]/div[@class='c-abstract']/text()")
        item['content'] = ''.join(abstract)
        list.append(item)
    # print(list)
    item_al['data'] = list
    item_al['type'] = 'bdjs'
    return item_al
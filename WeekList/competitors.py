#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 18:59:31 2022

@author: dawn
"""
# -*- codeing = utf-8 -*-
# 第三方库
import sys
import gzip
import re  # 正则表达式，进行文字匹配`
import urllib.error  # 制定URL，获取网页数据
import urllib.request
import time  # 引入time模块
import datetime
from io import BytesIO
import xlwt  # 进行excel操作
from bs4 import BeautifulSoup  # 网页解析，获取数据
# 自定义
import consts
import queryRule
import utils

# import sqlite3  # 进行SQLite数据库操作
# <a href="oneauthor.php?authorid=828396" target="_blank">漫漫何其多</a>
# 最大页数，系统最大常量赋值
pageMax = sys.maxsize
startPage = 1

# 当前时间戳
currentDayTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# 爬取数据的开始时间和结束时间
startPublishTime = utils.getTimeStamp('2022-07-25 00:00:00')
endPublishTime = utils.getTimeStamp('2022-08-07 23:59:59')

def main():
    baseurl = consts.Xianyan  # 要爬取的网页链接
    # 1.爬取网页
    datalist = getData(baseurl)
    savepath: str = "最新更新作品.xls"  # 当前目录新建XLS，存储进去
    # dbpath = "movie.db"              #当前目录新建数据库，存储进去
    # 3.保存数据
    saveData(datalist, savepath)  # 2种存储方式可以只选择一种
    # saveData2DB(datalist,dbpath)

# 获取novel详情
def getNovelDetail(novelID):
    novelUrl = consts.originNovelUrl + str(novelID)
    novelHtml = askURL(novelUrl)  # 保存获取到"novel"的网页源码
    # 2.逐一解析数据 # BeautifulSoup4将复杂的HTML文档转换成一个复杂的树形结物，每个节点都是Python对象
    novelSoup = BeautifulSoup(novelHtml, "html.parser")
    # list = novelSoup.find_all(text = re.compile("\d"))
    # novelSoup.select(#u1) novelSoup.select("a[class='bri']")
    isDelete = len(novelSoup.find_all(text="已签约")) == 0 and len(novelSoup.find_all(text="未签约")) == 0
    isContract = len(novelSoup.find_all(text="已签约")) > 0
    contractStatus = ''   # 签约状态
    favoritesNumber = 0  # 收藏数
    # print(novelSoup.find_all(text="晋江"), novelSoup.find_all(text="未签约"))
    if isContract:
        contractStatus = '已签约'
        favortiesLen = len(novelSoup.find_all(itemprop="collectedCount"))
        if favortiesLen > 0:
            favorties = str(novelSoup.find_all(itemprop="collectedCount")[0])
            favoritesNumber = int(re.findall(queryRule.findFavoritesNumber, favorties)[0])
        else:
            contractStatus = "文章已删除！"
    return isContract, contractStatus, favoritesNumber

# 爬取网页
def getData(baseurl):
    datalist = []  # 用来存储爬取的网页信息
    isBreak= False;
    for i in range(startPage, pageMax):  # 调用获取页面信息的函数，pageMax为系统最大值
        url = baseurl + str(i)
        html = askURL(url)  # 保存获取到"最新更新作品"的网页源码
        # 2.逐一解析数据
        soup = BeautifulSoup(html, "html.parser")
        # s = 0
        items = soup.find_all('tr')
        for item in items[1:]:  # 查找符合要求的字符串
            # print(str(s) + ":\n" + str(item))
            # s = s + 1
            data = []  # 保存一部电影所有信息
            item = str(item)
            # 发表时间
            publishTime = re.findall(queryRule.findTime, item)[0]
            publishTimeStamp = utils.getTimeStamp(publishTime)
            # print('publishTime', publishTime, startPublishTime, publishTimeStamp, publishTimeStamp < startPublishTime, publishTimeStamp >= startPublishTime and publishTimeStamp <= endPublishTime, i)
            if publishTimeStamp < startPublishTime:
                isBreak = True;
                break;
            if publishTimeStamp >= startPublishTime and publishTimeStamp <= endPublishTime:
                # 作者信息
                authorInfo = re.findall(queryRule.findAuthorInfo, item)[0]
                authorID = authorInfo[0]  # 通过正则表达式查找
                author = authorInfo[1]
                # 作品信息
                novel = re.findall(queryRule.findNovelInfo, item)
                hasNovel = len(novel) > 0
                novelID = ''
                title = ''
                if (hasNovel):
                    novelInfo = novel[0]
                    # print('novelInfo', novelInfo)
                    novelID = novelInfo[0]
                    title = novelInfo[3]
                # print('novelID', novelID)
                # intro = novelInfo[1]
                # tag = novelInfo[2]
                ntype = re.findall(queryRule.findType, item)
                CC = re.findall(queryRule.findCC, item)
                style = CC[0]
                progress = CC[1]
                Nums = re.findall(queryRule.findNums, item)
                wordCount = int(Nums[0])
                score = Nums[1]
                # data.append(publishTime)
                # print('novelID', novelID)
                # 获取签约状态、收藏数
                isContract, contractStatus, favoritesNumber = getNovelDetail(novelID)
                if isContract:
                    print('author', authorID, author, publishTime)
                    data.extend([authorID, author, novelID, title, favoritesNumber, contractStatus, ntype, style, progress, wordCount, score, publishTime])
                    datalist.append(data)
        if isBreak:
            break;
    return datalist

# 得到指定一个URL的网页内容
def askURL(url):
    head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / "
                      "80.0.3987.122  Safari / 537.36 ",
        "cookie": consts.Cookie,
    }
    # 用户代理，表示告诉豆瓣服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接收什么水平的文件内容）

    request = urllib.request.Request(url, headers=head)
    # post请求
    # data = bytes(urllib.parse.urlencode({ 'name': 'eric' }), encoding="utf-8")
    # request = urllib.request.Request(url, data, headers=head, method="POST")
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read()
        try:
            html = html.decode("gb18030")
        except:
            buff = BytesIO(html)
            f = gzip.GzipFile(fileobj=buff)
            html = f.read().decode("gb18030")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print('网络状态码', e.code)
        if hasattr(e, "reason"):
            print('报错原因',e.reason)
    return html


# 保存数据到表格
def saveData(datalist, savepath):
    print("save.......")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet('最新更新作品', cell_overwrite_ok=True)  # 创建工作表
    col = ("作者ID", "作者", "作品ID", "小说名称", "收藏数", "签约状态", "类型", "风格", "进度", "字数", "积分", "发表时间")
    for i in range(0, len(col)):
        sheet.write(0, i, col[i])  # 列名
    for i in range(0, len(datalist)):
        # print("第%d条" %(i+1))       #输出语句，用来测试
        data = datalist[i]
        for j in range(0, len(col)):
            sheet.write(i + 1, j, data[j])  # 数据
    book.save(savepath)  # 保存


# def saveData2DB(datalist,dbpath):
#     init_db(dbpath)
#     conn = sqlite3.connect(dbpath)
#     cur = conn.cursor()
#     for data in datalist:
#             for index in range(len(data)):
#                 if index == 4 or index == 5:
#                     continue
#                 data[index] = '"'+data[index]+'"'
#             sql = '''
#                     insert into movie250(
#                     info_link,pic_link,cname,ename,score,rated,instroduction,info)
#                     values (%s)'''%",".join(data)
#             # print(sql)     #输出查询语句，用来测试
#             cur.execute(sql)
#             conn.commit()
#     cur.close
#     conn.close()


# def init_db(dbpath):
#     sql = '''
#         create table movie250(
#         id integer  primary  key autoincrement,
#         info_link text,
#         pic_link text,
#         cname varchar,
#         ename varchar ,
#         score numeric,
#         rated numeric,
#         instroduction text,
#         info text
#         )
#
#
#     '''  #创建数据表
#     conn = sqlite3.connect(dbpath)
#     cursor = conn.cursor()
#     cursor.execute(sql)
#     conn.commit()
#     conn.close()

# 保存数据到数据库


if __name__ == "__main__":  # 当程序执行时
    # 调用函数
    main()
    # init_db("movietest.db")
    print("爬取完毕！")

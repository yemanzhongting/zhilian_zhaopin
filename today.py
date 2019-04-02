# -*- coding: UTF-8 -*-
__author__ = 'zy'
__time__ = '2019/4/1 23:13'
from urllib import request,parse
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import json
from jsonpath import jsonpath
import xlwt,time,random,hashlib


from xlrd import open_workbook
import xlrd
from xlutils.copy import copy

def write_excel_xls_append(path, value):
    index = len(value)  # 获取需要写入数据的行数
    workbook = xlrd.open_workbook(path)  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            new_worksheet.write(i+rows_old, j, value[i][j])  # 追加写入数据，注意是从i+rows_old行开始写入
    new_workbook.save(path)  # 保存工作簿
    print("xls格式表格【追加】写入数据成功！")
import requests,lxml
from lxml import etree
import pymongo
def savedb(dbname,data):
    client = pymongo.MongoClient('127.0.0.1', 27017)  # 缺少一步骤进行属性的清洗操作，确定是否有这个值
    db = client.weibo
    db[dbname].insert(data)


def pase_page(page):
    md5 = hashlib.md5()
    id = str(random.random())
    md5.update(id.encode('utf-8'))
    random_id = md5.hexdigest()
    # 2、生成当前时间戳
    now_time = int(time.time() * 1000)
    # 3、生成随机6位数
    randomnumb = int(random.random() * 1000000)
    # 组合代码
    x_zp_page_request_id = str(random_id) + '-' + str(now_time) + '-' + str(randomnumb)
    url_v = round(random.random(), 8)

    data={
            'start':page,
            'pageSize':90,
            'cityId':530,
            'workExperience': -1,
            'education': -1,
            'companyType': -1,
            'employmentType': -1,
            'jobWelfareTag''': -1,
            'kw':'python',
            'kt':3,
            '_v': url_v,
            'x-zp-page-request-id': x_zp_page_request_id
        }
    url = 'https://fe-api.zhaopin.com/c/i/sou?' + urlencode(data)
    #两个data容易混淆
    header = {
        'Origin': 'https://sou.zhaopin.com',
        'Referer': 'https://sou.zhaopin.com/?jl=530&kw=python&kt=3&sf=0&st=0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
    }
    rsp = request.Request(url, headers=header)
    print(url)
    rsp = request.urlopen(rsp)
    json_data = rsp.read()
    data = json.loads(json_data)
    WORK_NAME = jsonpath(data, '$..jobName')
    SALARY = jsonpath(data, '$..salary')
    COMPANY = jsonpath(data, '$..company.name')
    COMPANY_TYPE = jsonpath(data, '$..company.type.name')
    COMPANY_URL = jsonpath(data, '$..positionURL')
    ADDRES=jsonpath(data, '$..city.display')
    #jobType
    jobType = jsonpath(data, '$..jobType.display')
    eduLevel=jsonpath(data, '$..eduLevel.name')
    workingExp=jsonpath(data, '$..workingExp.name')
    # 地址,经验,学历,职位信息


    #print(len(SALARY))
    #Header = ['工作名称', '薪水', '公司名称', '公司类型', '详细网页地址']

    L1 = list()
    L2 = list()
    L3 = list()
    L4 = list()
    L5 = list()
    L6 = list()
    L7 = list()
    L8 = list()
    L9 = list()
    L10=list()
    for x in WORK_NAME:
        L1.append(x)
    for x in SALARY:
        L2.append(x)
    for x in COMPANY:
        L3.append(x)
    for x in COMPANY_TYPE:
        L4.append(x)
    for x in COMPANY_URL:
        L5.append(x)

    for x in ADDRES:
        L6.append(x)
    for x in jobType:
        L7.append(x)
    for x in eduLevel:
        L8.append(x)
    for x in workingExp:
        L9.append(x)

    for i in range(len(L1)):

        detail_header = {
            'Referer': url,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
        }

        req=requests.get(L5[i],headers=header)
        html = etree.HTML(req.content)
        detail = html.xpath('//div[@class="job-detail"]//text()')
        detail=' '.join(detail)
        m_data = {
            'WORK_NAME': L1[i],
            'SALARY': L2[i],
            'COMPANY': L3[i],
            'COMPANY_TYPE': L4[i],
            'POST_URL': L5[i],
            'ADDRES': L6[i],
            'jobType': L7[i],
            'eduLevel': L8[i],
            'workingExp': L9[i],
            'detail':detail
        }
        print(detail)
        # if detail==None:
        #     req = requests.get(L5[i], headers=header)
        #     html = etree.HTML(req.content)
        #     detail = html.xpath('//div[@class=“job-detail”]//text()')

            # if detail==None:
            #     print('没有数据')
            #     detail='没有数据'
            # m_data['detail']=detail
        savedb('智联详情页',m_data)
    if len(L1)>1:
        print('再次抓取')
        time.sleep(2)
        page=int(page)+90
        print(page)
        pase_page(page)

    # wkb = xlwt.Workbook()
    # sheet = wkb.add_sheet('招聘信息', cell_overwrite_ok=True)
    # a = 0
    # b = 0
    # for head in range(len(Header)):
    #     sheet.write(a, head, Header[head])
    #
    # # 信息
    # for i in range(len(L1)):
    #     sheet.write(a + 1, b, L1[i])
    #     sheet.write(a + 1, b + 1, L2[i])
    #     sheet.write(a + 1, b + 2, L3[i])
    #     sheet.write(a + 1, b + 3, L4[i])
    #     sheet.write(a + 1, b + 4, L5[i])
    #     a = a + 1
    #     c0 = sheet.col(0)
    #     c0.width = 256 * 36
    #
    #     c2 = sheet.col(2)
    #     c2.width = 256 * 34
    #
    #     c3 = sheet.col(3)
    #     c3.width = 256 * 13
    #
    #     c4 = sheet.col(4)
    #     c4.width = 256 * 100
    #
    # wkb.save('招聘信息表升级版2.xls')


if __name__=='__main__':
    pase_page(0)




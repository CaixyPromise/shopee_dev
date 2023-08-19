# -*- coding: utf-8 -*-
import time
import requests
import re
import pandas as pd
from model import Goods, DataCleanner, SearchNode
import asyncio

class PDDSpider:
    _instance = None
    __cookie = None
    __key = None
    __pattern = r'window\.rawData\s*=\s*(\{.*?\});'

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, cookie = None):
        self.__session = requests.Session()
        self.__rowData = re.compile(pattern = self.__pattern)
        if (cookie is not None):
            self.set_cookie(cookie)

    async def fetch_details_page(self, dataNode : SearchNode):
        # 爬取商品信息
        response = self.__session.get(dataNode['goodsUrl'])
        html = response.text
        match = self.__rowData.search(html)
        result = ''

        if (match):
            data = match.group(1)
            result = Goods(await DataCleanner(data))
        else:
            result = "未找到匹配的数据"
        return result

    def fetch_search_data(self, key):
        response = self.__session.get(self.__search_url, headers = self.headers,
                                      cookies = self.__session.cookies)
        html = response.text
        datas = re.findall('"tagList":\[(.*?)"thumbWM":""', html)
        for data in datas:
            dataNode = SearchNode()
            # 商品名称
            goodsName = re.findall('"goodsName":"(.*?)"', data)[0].replace('\\u002F', '/')
            # 商品链接
            goodsUrl = ('https://mobile.yangkeduo.com/' + re.findall('"linkURL":"(.*?)"', data)[0]).replace('\\u002F', '/')
            # 销售信息
            salesTip = re.findall('"salesTip":"(.*?)"', data)[0].replace('\\u002F', '/')
            # 价格信息
            priceInfo = re.findall('"priceInfo":"(.*?)"', data)[0].replace('\\u002F', '/')

            dataNode['goodsName'] = goodsName
            dataNode['goodsUrl'] = goodsUrl
            dataNode['salesTip'] = salesTip
            dataNode['priceInfo'] = priceInfo
            yield dataNode

    def set_key(self, key):
        self.__key = key
        self.__search_url = f'https://mobile.yangkeduo.com/search_result.html?search_key={self.__key}&refer_page_name=login'

    def set_cookie(self, cookie):
        self.__cookie = cookie
        self.headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
                'cookie'    : cookie}
        self.__session.headers.update(self.headers)

    # def data2csv(self):
    #     data_frame = pd.DataFrame(
    #                 {
    #                     '商品名称': self.goods_list[0],
    #                     '商品链接': self.goods_list[1],
    #                     '销售信息': self.goods_list[2],
    #                     '价格信息': self.goods_list[3],
    #                     '拼团价'  : self.goods_list[4],
    #                     '颜色分类': self.goods_list[5],
    #                     '尺码'    : self.goods_list[6],
    #                 }
    #             )
    #     data_frame.to_csv('pdd_data.csv', index = False, encoding = 'utf_8_sig')

if __name__ == '__main__':
    cookies = r'api_uid=Ckp4NGScPIownwB1MYFoAg==; njrpl=xkQqzESTug2Nu9jndwfahqWAzAoQzVSQ; dilx=fzu7atcnkFg4EtVpVGTMc; webp=1; _nano_fp=XpEbX5gxX0dyn5Tqno_P~X~F_3zEyjyMWHFf5L98; jrpl=xkQqzESTug2Nu9jndwfahqWAzAoQzVSQ; PDDAccessToken=HSZZM4D5FDXPD7AA2BBLJZPEH4B77KGDYDEYBGSKODINWRVPHUMA120af35; pdd_user_id=3750380719; pdd_user_uin=JCASQXBAMT7DCFPI3XD5B5IWPE_GEXDA; pdd_vds=gaLcNdOwtmaBLBixydLsImQlNcPdmuLdibGxLbLLbLETmdEwbbyeODOxOdid'
    solution = PDDSpider(cookies)
    solution.set_key('iPhone')
    for v in solution.fetch_search_data(cookies):
        # try:
        print(asyncio.run(solution.fetch_details_page(v)))
    # except Exception as E:
    #     print(f'except: {v}')
    #     print(f'info:{repr(E)}, line: {E.__traceback__.tb_lineno}')
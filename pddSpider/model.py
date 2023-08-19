from json import loads, dumps
from typing import List, Optional, Dict
import asyncio

class SearchNode:
    goodsName: str = 0  # 商品名称
    goodsUrl: str = 0  # 商品链接
    salesTip: str = 0  # 销售信息
    priceInfo: int = 0  # 价格信息
    groupPrice: int = 0  # 拼团价格
    size: str = 0  # 尺寸

    def __dict__(self):
        return {
            '商品名称': self.goodsName,
            '商品链接': self.goodsUrl,
            '销售信息': self.salesTip,
            '价格信息': self.priceInfo,
            '拼团信息': self.groupPrice,
            '商品尺寸': self.size
            }

    def __str__(self):
        return dumps(self.__dict__(), ensure_ascii = False)

    def __setitem__(self, key, value):
        setattr(self, key, value)
        return self

    def __getitem__(self, item):
        return getattr(self, item, None)


class Goods:
    goodsID: int = None  # 商品ID
    goodsName: str = None  # 商品名称
    goodsUrl: str = None  # 商品链接
    salesTip: str = None  # 销售信息
    goodsSpec: List[Optional[Dict[str, str]]] = None  # 商品详情配置
    TopGallery: List[Optional[str]] = None  # 顶部翻转图
    videoGallery: List[Optional[str]] = None  # 视频链接
    BottomGallery: List[Optional[Dict[str, str]]] = None  # 底部详情介绍图
    OrderSpec: List[Optional[Dict[str, str]]] = None  # 商品点击下单时所支持的选项
    PromiseService: List[Optional[Dict[str, str]]] = None  # 商品承诺服务
    OrderTips: str = None  # 商品备注

    def __init__(self, kwargs):
        [setattr(self, key, value) for key, value in kwargs.items()]

    def to_dict(self):
        return {
            '商品ID' :   self.goodsID,
            '商品名称':   self.goodsName,
            '商品链接':   self.goodsUrl,
            '销售信息':   self.salesTip,
            '商品参数':   self.goodsSpec,
            '顶部翻转图': self.TopGallery,
            '底部详情图': self.BottomGallery,
            '视频链接':   self.videoGallery,
            '下单配置':   self.OrderSpec,
            '承诺服务':   self.PromiseService,
            '下单提示':   self.OrderTips
            }

    def __str__(self):
        return dumps(self.to_dict(), ensure_ascii = False, indent = 4)

    def __setitem__(self, key, value):
        setattr(self, key, value)
        return self

    def __getitem__(self, item):
        return getattr(self, item, None)

class JsonDecode:
    def __init__(self, json_text: str):
        self._init(json_text)

    def _init(self, json_text: str):
        json_text = json_text.replace('\\u002F', '/')
        self.__json_body = loads(json_text)
        self.__json_data = self.__json_body['store']

    def set(self, json_text):
        self._init(json_text = json_text)

    @property
    def keys(self):
        return set(self.__json_data)

    @property
    def text(self):
        return dumps(self.__json_body, ensure_ascii = False, indent = 4)

    def __adjust(self, item):
        if (item in self.__json_data.keys()):
            self.__json_data = self.__json_data[item]
        else:
            return False

    def adjust_Direction(self, items, init = None):
        if (init is True):
            self.__json_data = self.__json_body['store']
        else:
            while 1:
                if (isinstance(items, list)):
                    for item in (items):
                        if (self.__adjust(item) is False):
                            return self.__json_data
                else:
                    self.__adjust(items)
                    return self.__json_data
        return self.__json_data

    def get(self, item):
        return self[item]

    def __getitem__(self, item):
        return self.__json_data.get(item, None)

    def __str__(self):
        return self.text


class DataCleanner:
    # _instance = None

    def __init__(self, json_text: str):
        self.set_json(json_text)

    # def __new__(cls, *args, **kwargs):
    #     if cls._instance is None:
    #         cls._instance = super().__new__(cls)
    #     return cls._instance

    def __await__(self):
        return self.run().__await__()

    def set_json(self, json_text: str):
        self.__json_body = JsonDecode(json_text)
        self.__json_body.adjust_Direction('initDataObj')
        self.__json_data = self.__json_body.adjust_Direction('goods')
        self.__json_key = set(self.__json_data.keys())
        self.__results = {}

    async def clean_default_data(self):
        self.__results['goodsID'] = self.__json_data['goodsID']
        self.__results['goodsName'] = self.__json_data['goodsName']
        self.__results['salesTip'] = self.__json_data['sideSalesTip']

    async def clean_skus(self):
        sku_results = []
        sku_append = sku_results.append
        for skus in self.__json_data['skus']:
            specs_result = dict()
            for specs in skus['specs']:
                specs_result.update({specs['spec_key']: specs['spec_value']})
            specs_result.update({"拼团价格": skus['groupPrice']})
            specs_result.update({"不拼团价": skus['normalPrice']})
            specs_result.update({"商品原价": round(skus['oldGroupPrice'] / 100, 2)})
            specs_result.update({"型号预览": skus['thumbUrl']})
            specs_result.update({"最大限购": skus['limitQuantity']})
            specs_result.update({"商品库存": skus['quantity']})
            sku_append(specs_result)

        self.__results["OrderSpec"] = sku_results

    async def clean_view_image_data(self):
        self.__results["TopGallery"] = self.__json_data['viewImageData']

    async def clean_detail_gallery(self):
        self.__results["BottomGallery"] = self.__json_data['detailGallery']

    async def clean_video_gallery(self):
        self.__results['videoGallery'] = self.__json_data['videoGallery']

    async def clean_goods_property(self):
        property_results = []
        for data_config in self.__json_data['goodsProperty']:
            property_results.append({'key': data_config['key'], 'value': data_config['values'][0]})
        self.__results["goodsSpec"] = property_results

    async def clean_mall_service(self):
        service_results = []
        for service in self.__json_data['mallService']['service']:
            service_results.append({service['type']: service['desc']})
        self.__results["PromiseService"] = service_results

    async def clean_share_link(self):
        self.__results["goodsUrl"] = 'https://mobile.yangkeduo.com/' + self.__json_data['shareLink']

    async def clean_prompt_explain(self):
        if ('promptExplain' in self.__json_key):
            self.__results["OrderTips"] = self.__json_data['promptExplain']

    async def run(self):
        self.__results.clear()
        await asyncio.gather(
                self.clean_default_data(),
                self.clean_skus(),
                self.clean_view_image_data(),
                self.clean_detail_gallery(),
                self.clean_video_gallery(),
                self.clean_goods_property(),
                self.clean_mall_service(),
                self.clean_share_link(),
                self.clean_prompt_explain()
                )
        return self.__results


if __name__ == '__main__':
    with open('../goodDetails.json', 'r', encoding = 'utf-8') as fp:
        jsonText = fp.read()
    cleaner = DataCleanner(jsonText)
    result = asyncio.run(cleaner.run())
    print(dumps(Goods(result).to_dict(), ensure_ascii = False, indent = 4))
    # print(type(result))
    # print(Goods(result).to_dict())
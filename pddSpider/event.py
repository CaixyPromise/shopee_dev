# from CookiePool import *
# from ThreadPool import *
from spider import *
import asyncio
import configparser

class Config:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def sections(self):
        return self.__sections

    def __init__(self):
        self.__config = configparser.ConfigParser()
        self.__config.read('config.ini')
        self.__sections = set(self.__config.sections())

    def get(self, item):
        """返回所有选项（options）的列表
        config.options('section_name')
        """
        if (item in self.__sections):
            return self.__config.options(item)
        return None

    def get_option_value(self, item, value):
        """返回指定选项的值
        config.get('section_name', 'option_name')
        """
        if (self.get(item) is not None):
            return self.__config.get(item, value)
        return None

    def get_option_dict(self, section):
        section_dict = {}
        for option in self.get(section):
            section_dict[option] = self.get_option_value(section, option)
        return section_dict

    def all_to_dict(self):
        """把全部参数集合到字典内"""
        config_dict = {}
        for section in self.__sections:
            config_dict[section] = self.get_option_dict(section)
        return config_dict

class PDDEvent:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.__spider = PDDSpider()


    def set_cookie(self, cookie):
        self.__spider.set_cookie(cookie)

    def search_goods(self, key):
        self.__spider.set_key(key)
        self.__spider.fetch_search_data(key)

    def get_details_page(self, dataNode : SearchNode):
        # self.__spider
       return asyncio.run(self.__spider.fetch_details_page(dataNode))

import asyncio
from tkinter.ttk import Treeview, Button, Scrollbar, Frame
from tkinter import Toplevel, Label, LabelFrame
import webbrowser
import re
from pddSpider.model import Goods, DataCleanner


class TreeViewUtils(Treeview):
    def __init__(self, parent, column_width = 100, **args):
        Treeview.__init__(self, parent, **args)

        self.pack(fill = 'both', expand = True)
        for column in self['columns']:
            self.column(column, width = column_width, anchor = 'center')
            self.heading(column, text = column, )

    def config(self, item, value):
        self.config(item = item, value = value)

    def insert_data(self, values, parent = '', index = 'END', item = None):
        self.insert(parent, index, item, values = values)

    def sort_tree(self, tree, col, reverse, func):
        l = [(tree.set(k, col), k) for k in tree.get_children('')]
        l.sort(key = func, reverse = reverse)
        for index, (val, k) in enumerate(l):
            tree.move(k, '', index)
        tree.heading(col, command = lambda _col = col: self.sort_tree(tree, _col, not reverse, func))

    def delete_item(self, item):
        self.delete(item)

    def update_item(self, item, values):
        for i, value in enumerate(values):
            self.item(item, values = (value,))

    def search_item(self, values, index):
        for item in self.get_children():
            if self.item(item)["values"][index] == values:
                return item
        return None

    def bindEvent(self, event_name, func):
        self.bind(event_name, func)


class ToplevelUtils(Toplevel):
    def __init__(self, parent, title):
        super().__init__(parent)
        self.title(title)
        # self.geometry(f'{width}x{height}+{self.winfo_screenwidth()}+{self.winfo_screenheight()}')


class DataDetailsTable(ToplevelUtils):
    __regex = r"(https?://|www\.)[^\s/$.?#].[^\s]*"
    _isLink = re.compile(__regex)

    def __init__(self, parent, title, dataNode):
        super().__init__(parent, title)
        self.dataNode = dataNode

        self.goodsTitleFrame = LabelFrame(self, text = '商品详情')
        self.goodsTitleFrame.pack(padx = (10, 10), pady = (10, 10), fill = "both", expand = True)
        self.show_goodsNode()

    @classmethod
    def is_link(cls, text):
        return cls._isLink.match(text) is not None

    def show_goodsNode(self):
        id_frame = Frame(self.goodsTitleFrame)
        id_frame.pack(side = 'top', padx = 5, pady = 5, expand = True, fill = 'both')
        name_frame = Frame(self.goodsTitleFrame)
        name_frame.pack(side = 'top', padx = 5, pady = 5, expand = True, fill = 'both')
        url_frame = Frame(self.goodsTitleFrame)
        url_frame.pack(side = 'top', padx = 5, pady = 5, expand = True, fill = 'both')
        Label(id_frame,
              text = f"商品ID: {self.dataNode.goodsID}",
              font = ("Arial", 12)
              ).pack(
                side = 'left', pady = 5, padx = 5
                )
        Label(name_frame,
              text = f"商品名称: {self.dataNode.goodsName}",
              font = ("Arial", 12)
              ).pack(
                side = 'left', pady = 5, padx = 5
                )
        Button(url_frame,
               text = "商品链接",
               command = lambda: webbrowser.open(self.dataNode.goodsUrl)
               ).pack(
                side = 'left', pady = 5, padx = 5
                )

        self.setup_treeview('商品参数', callback = self.insert_goodDetails, part_configure = self.details_configure )
        self.setup_treeview('下单配置', columns = ('属性', '内容'), part_configure = self.OrderTree_configure,
                            callback = self.insert_orderSpec, )
        # Label()
    @staticmethod
    def OrderTree_configure(frame, columns, show, yscrollcommand):
        tree = TreeViewUtils(frame)
        tree["columns"] = ["key", "value"]
        tree.heading("key", text = "属性")
        tree.heading("value", text = "内容")
        tree.column("key", width = 150, anchor = "w")
        tree.column("value", width = 300, anchor = "w")
        return tree
    @staticmethod
    def details_configure(frame, columns, show, yscrollcommand):
        return TreeViewUtils(frame, columns = columns, show = show,
                                      yscrollcommand = yscrollcommand)
    @staticmethod
    def insert_goodDetails(tree, value):
        # 插入商品参数，展现列表形式
        [tree.insert('', 'end', values = (val_dict['key'], val_dict['value'])) for val_dict in value]
    @staticmethod
    def insert_orderSpec(tree, value):
        # 插入下单配置，展现树状图形式
        for idx, config in enumerate(value):
            parent = tree.insert('', 'end', text = f"配置 {idx + 1}")
            for sub_key, sub_value in config.items():
                tree.insert(parent, 'end', values = (sub_key, sub_value))

    def setup_treeview(self, key, callback, part_configure, columns = ('属性', '内容'), show = "headings" ):
        """为指定的 key 设置 Treeview"""
        frame = LabelFrame(self, text = key)
        frame.pack(pady = 10, fill = "both", expand = True)
        data = self.dataNode.to_dict()
        self.scro_ball = Scrollbar(frame)

        self.tree = part_configure(frame, columns, show, self.scro_ball)
        self.scro_ball.config(command = self.tree.yview)
        self.tree.bind()
        value = data.get(key, {})
        callback(tree = self.tree, value = value)
        self.tree.pack(fill = "both", expand = True)


if __name__ == '__main__':
    import json
    import tkinter as tk

    with open('goodDetails.json', 'r', encoding = 'utf-8') as fp:
        goods_data = (fp.read())
    win = tk.Tk()
    cleaner = DataCleanner(goods_data)

    result = asyncio.run(cleaner.run())
    window = DataDetailsTable(win, title = 'test', dataNode = Goods(result))
    window.title("商品详情")
    window.mainloop()

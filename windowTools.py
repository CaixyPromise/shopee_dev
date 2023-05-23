from tkinter.ttk import Treeview
from tkinter import Toplevel, Label, LabelFrame
import webbrowser
import re


class TreeViewUtils(Treeview):
    def __init__(self, parent, pack_now = True, **args):
        Treeview.__init__(self, parent,  **args)
        self.__pack_now = pack_now
        if self.__pack_now:
            self.pack(fill = 'both', expand = True)
        for column in self['columns']:
            self.column(column, width = 70, anchor = 'center')
            self.heading(column, text = column,
                         command = lambda _col = column: self.sort_tree(self, _col, False))

    # def __init__(self, parent, columns, pack_now = True,  column_width = 100, **kwags):
    #     Treeview.__init__(self, parent, **kwags)
    #     self.__pack_now = pack_now
    #     if (self.__pack_now is True):
    #         self.pack(fill = 'both', expand = True)
    #         print('pack_now')
    #     for col in self['columns']:
    #         self.column(col, width = column_width, anchor = kwags.get('anchor', 'center'))
    #         self.heading(col, text = col )
    #
    def pack_part(self, parent = None):
        if (not self.__pack_now):
            if (parent is None):
                self.pack(fill = 'both', expand = True)
            else:
                self.pack(in_ = parent, expand = True, fill = 'both')

    def insert_data(self, values, parent = '', index = 'end', item = None):
        self.insert(parent, index, item, values = values)

    def sort_tree(self, tree, col, reverse):
        l = [(tree.set(k, col), k) for k in tree.get_children('')]
        l.sort(key = lambda t: t[0], reverse = reverse)

        for index, (val, k) in enumerate(l):
            tree.move(k, '', index)
        tree.heading(col, command = lambda _col = col: self.sort_tree(tree, _col, not reverse))

    def delete_item(self, item):
        self.delete(item)

    def update_item(self, item, values):
        for value in values:
            self.item(item, values = (value,))

    def search_item(self, values):
        for item in self.get_children():
            if self.item(item)["values"] == values:
                return item
        return None

    def bindEvent(self, event_name, func, need_self = False, **kwargs):
        if (need_self is True):
            self.bind(event_name, lambda event : [func(event, self, kwargs)])
        self.bind(event_name, lambda event : [func(event, kwargs)])


class ToplevelUtils(Toplevel):
    __regex = r"(https?://|www\.)[^\s/$.?#].[^\s]*"
    _isLink = re.compile(__regex)

    def __init__(self, parent, title, width, height):
        super().__init__(parent)
        self.title(title)
        self.geometry(f'{width}x{height}+{self.winfo_screenwidth()}+{self.winfo_screenheight()}')

    @classmethod
    def is_link(cls, text):
        return cls._isLink.match(text) is not None

    @classmethod
    def push_list_tree(cls, list_view : TreeViewUtils, _type, content):
        if (isinstance(content, dict)):
            cls.push_dict_tree(list_view, content = content)
        else:
           [ list_view.insert_data((_type, val, '打开链接')) for val in content ]

    @classmethod
    def push_dict_tree(cls, list_view : TreeViewUtils, content : dict):
        for key, value in content.items():
            if (isinstance(value, list)):
                cls.push_list_tree(list_view, key, value)
            else:
                list_view.insert_data((key, value, '打开链接'))

    @staticmethod
    def open_url(event, tree, kwargs):
        item_id = tree.identify_row(event.y)
        column = tree.identify_column(event.x)
        if column == "#2":
            webbrowser.open(kwargs['url'])

    @classmethod
    def show_goodsNode_info(cls, dataNode, parent, **win_config):
        info_win = cls(parent, **win_config)
        Link_viewer = TreeViewUtils(info_win, columns = ('数据类型', '数据内容', '打开链接'), pack_now = False)


        config_pad = {'padx' : (10, 10), 'pady' : (10, 10)}

        base_info = LabelFrame(info_win, text = '商品基础信息')
        # base_info.pack(fill = 'both', expand = True)

        goods_info = LabelFrame(info_win, text = '商品参数信息')
        # goods_info.pack(fill = 'both', expand = True)

        order_info = LabelFrame(info_win, text = '下单配置')
        # order_info.pack(fill = 'both', expand = True)

        PromiseService = LabelFrame(info_win, text = '商家服务')
        # PromiseService.pack(fill = 'both', expand = True)

        order_tips = LabelFrame(info_win, text = '下单提醒')
        # order_tips.pack(fill = 'both', expand = True)
        row_count = 0
        col_count = 0

        for key, value in dataNode.__dict__.items():
            match key:
                case '商品ID' | '商品名称' | '销售信息':
                    Label(base_info, text = f"{key}: {value}", font = 18).grid(row= row_count, column = col_count,
                                                                               **config_pad)
                    if (col_count == 0):
                        col_count += 1
                    if (col_count == 1):
                        col_count = 0
                        row_count += 1
                case '商品链接':
                    Label(base_info, text = '商品链接: 打开链接', font = 18).grid(row = row_count, column = col_count,
                                                                                **config_pad)
                case '商品参数':
                    config_row, config_col = 0, 0
                    for configDict in value:
                        Label(goods_info, text = f'{configDict["key"]}: {configDict["value"]}')
                case '顶部翻转图':
                    pass
                    # Link_viewer.insert_data()
                case '底部详情图':
                    pass
                case '视频链接':
                    pass
                case '下单配置':
                    pass
                case '承诺服务':
                    pass
                case '下单提示':
                    pass
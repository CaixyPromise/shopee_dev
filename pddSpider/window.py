import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import requests


class TreeViewClass(ttk.Treeview):
    def __init__(self, parent, **args):
        ttk.Treeview.__init__(self, parent, **args)

        self.pack(fill = 'both', expand = True)

        for i, column in enumerate(self['columns']):
            self.column(column, width = 100, anchor = tk.CENTER)
            self.heading(column, text = column,
                              command = lambda _col = column: self.sort_tree(self, _col, False)
                              )

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
        for i, value in enumerate(values):
            self.item(item, values = (value,))

    def search_item(self, values):
        for item in self.get_children():
            if self.item(item)["values"] == values:
                return item
        return None

    def bindEvent(self, event_name, func):
        self.bind(event_name, func)



class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.master = parent
        self.__keyword_VAL = tk.StringVar()

        self.setupFrame()


    def setupFrame(self):
        self.__CommandFrame = ttk.LabelFrame(self, text = '控制台')
        self.__CommandFrame.grid(row = 0, column = 0, padx = (20, 10), pady = (20, 10))
        self.__ListFrame = ttk.LabelFrame(self, text = '商品列表')
        self.__ListFrame.grid(row = 0, column = 1, padx = (20, 10), pady = (20, 10))
        self.__TaskFrame = ttk.LabelFrame(self, text = '任务列表')
        self.__TaskFrame.grid(row = 0, column = 2, padx = (20, 10), pady = (20, 10))
        self.__resultFrame = ttk.LabelFrame(self, text = '状态')
        self.__resultFrame.grid(row = 1, column = 0, columnspan = 3,sticky = 'E', padx = (20, 10), pady = (20, 10))

        self.setupTopPart()


    def setupTopPart(self):
        # 信息输入框
        SPACING = 10
        LABEL_WIDTH = 10

        ttk.Label(self.__CommandFrame, text = '关键字：', width = LABEL_WIDTH, font = 15).grid(row = 0, column = 0, sticky = "W",
                                                                                   padx = (SPACING, 0)
                                                                                   )
        ttk.Entry(self.__CommandFrame, textvariable = self.__keyword_VAL).grid(row = 0, column = 1, sticky = "W",
                                                                               padx = (0, SPACING),
                                                                               pady = (0, SPACING)
                                                                               )

        ttk.Button(self.__CommandFrame, text = '开始爬虫搜索').grid(row = 1, column = 0, padx = (SPACING, 0),
                                                                pady = (SPACING, SPACING ), sticky = 'E'
                                                                )
        ttk.Button(self.__CommandFrame, text = '开始爬虫任务').grid(row = 1, column = 1, padx = (0, SPACING),
                                                                pady = (SPACING, SPACING), sticky = 'E'
                                                                )

        ttk.Button(self.__CommandFrame, text = '管理Cookie池').grid(row = 2, column = 0, padx = (SPACING, 0),
                                                                    pady = (SPACING, SPACING), sticky = 'E'
                                                                    )
        ttk.Button(self.__CommandFrame, text = '结束爬虫任务').grid(row = 2, column = 1, padx = (0, SPACING),
                                                                pady = (SPACING, SPACING), sticky = 'E'
                                                                )
        ttk.Button(self.__CommandFrame, text = '退出系统').grid(row = 3, column = 0, columnspan = 2, sticky = "NSEW",
                                                                padx = (SPACING, SPACING), pady = (SPACING, SPACING)
                                                                )
        self.__CommandFrame.columnconfigure(0, weight = 1)
        self.__CommandFrame.columnconfigure(1, weight = 1)

        # 绘制搜索结果
        self.SearchBox = TreeViewClass(self.__ListFrame,
                                       columns = ('关键词', '链接', '价格', '店铺名称', '添加任务'),
                                       show = "headings",
                                       selectmode = tk.EXTENDED,
                                       )
        self.SearchBox.insert_data(['12', '21', '312', '31', '345'])

    def setupBottomPart(self):
        pass

def main():
    root = tk.Tk()
    root.title("拼多多爬取平台_vBeta 0.1_CAIXYPROMISE")

    root.tk.call("source",    "theme/azure.tcl")
    root.tk.call("set_theme", "light")

    app = App(root)
    app.pack(fill = "both", expand = True)
    root.update_idletasks()

    width, height = root.winfo_width(), root.winfo_height()
    x = int((root.winfo_screenwidth() / 2) - (width / 2))
    y = int((root.winfo_screenheight() / 2) - (height / 2))

    root.minsize(width, height)
    root.geometry(f"+{x}+{y}")
    root.mainloop()

if __name__ == '__main__':
    main()
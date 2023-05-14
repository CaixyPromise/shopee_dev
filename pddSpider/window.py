import tkinter as tk
from tkinter import ttk
from windowTools import TreeViewUtils
from event import *

class TreeViewClass(TreeViewUtils):
    def __init__(self, parent, **kwags):
        TreeViewUtils.__init__(self, parent, **kwags)

class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.master = parent
        self.__keyword_VAL = tk.StringVar()
        self.setupFrame()

        # PDDEvent().

    def setupFrame(self):
        self.__CommandFrame = ttk.LabelFrame(self, text = '控制台')
        self.__CommandFrame.grid(row = 0, column = 0, padx = (20, 10), pady = (20, 10), sticky = 'NSEW')
        self.__ListFrame = ttk.Frame(self)
        self.__ListFrame.grid(row = 0, column = 1, padx = (20, 10), pady = (20, 0), sticky = 'NSEW')
        self.__TaskFrame = ttk.LabelFrame(self, text = '任务列表    ')
        self.__SearchFrame = ttk.LabelFrame(self, text = '搜索结果')
        self.__resultFrame = ttk.LabelFrame(self, text = '状态')
        self.__resultFrame.grid(row = 1, column = 0, columnspan = 2,sticky = 'NSEW', padx = (20, 10), pady = (5, 10))

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.setupTopPart(username = 'caixy')
        self.setupBottomPart()

    def setupTopPart(self, **kwargs):
        # 信息输入框
        SPACING = 10
        LABEL_WIDTH = 10
        ttk.Label(self.__CommandFrame, text = '欢迎回来: {}'.format(kwargs.get('username')), font = 15).grid(
                column = 0, row = 0, sticky = "W", padx = (SPACING, 0))

        ttk.Label(self.__CommandFrame, text = '关键字：', width = LABEL_WIDTH, font = 15).grid(row = 1, column = 0, sticky = "W",
                                                                                   padx = (SPACING, 0))
        ttk.Entry(self.__CommandFrame, textvariable = self.__keyword_VAL, width = 15).grid(row = 1, column = 1,
                                                      sticky = "W", padx = (0, SPACING), pady = (0, SPACING))
        ttk.Button(self.__CommandFrame, text = '开始爬虫搜索').grid(row = 2, column = 0, sticky = "NSEW",
                                                      padx = (SPACING, SPACING), pady = (SPACING, SPACING))
        ttk.Button(self.__CommandFrame, text = '开始爬虫任务').grid(row = 2, column = 1, sticky = "NSEW",
                                                      padx = (SPACING, SPACING), pady = (SPACING, SPACING))
        ttk.Button(self.__CommandFrame, text = '管理Cookie池').grid(row = 3, column = 0, sticky = "NSEW",
                                                      padx = (SPACING, SPACING), pady = (SPACING, SPACING))
        ttk.Button(self.__CommandFrame, text = '结束爬虫任务').grid(row = 3, column = 1, sticky = "NSEW",
                                                      padx = (SPACING, SPACING), pady = (SPACING, SPACING))
        ttk.Button(self.__CommandFrame, text = '账号信息',).grid(row = 4, column = 0, sticky = "NSEW",
                                                      padx = (SPACING, SPACING), pady = (SPACING, SPACING))
        ttk.Button(self.__CommandFrame, text = '修改密码',).grid(row = 4, column = 1,  sticky = "NSEW",
                                                      padx = (SPACING, SPACING), pady = (SPACING, SPACING))
        ttk.Button(self.__CommandFrame, text = '使用帮助', ).grid(row = 5, column = 0,  sticky = "NSEW",
                                                      padx = (SPACING, SPACING), pady = (SPACING, SPACING))
        ttk.Button(self.__CommandFrame, text = '订阅信息',).grid(row = 5, column = 1,  sticky = "NSEW",
                                                      padx = (SPACING, SPACING), pady = (SPACING, SPACING))
        ttk.Button(self.__CommandFrame, text = '退出系统').grid(row = 6, column = 0, columnspan = 2, sticky = "NSEW",
                                                      padx = (SPACING, SPACING), pady = (SPACING, SPACING))
        self.__CommandFrame.columnconfigure(0, weight = 1)
        self.__CommandFrame.columnconfigure(1, weight = 1)

        Searchscrollbar = ttk.Scrollbar(self.__SearchFrame)
        Searchscrollbar.pack(side = "right", fill = "y")

        # 绘制搜索结果
        self.SearchBox = TreeViewClass(self.__SearchFrame,
                                       columns = ('关键词', '链接', '价格', '店铺名称', '添加任务'),
                                       show = "headings",
                                       yscrollcommand = Searchscrollbar)
        self.SearchBox.insert_data(['12', '21', '312', '31', '开始任务'])

        # 绘制任务列表
        TaskScrollBar = ttk.Scrollbar(self.__TaskFrame)
        TaskScrollBar.pack(side = "right", fill = "y")
        self.TaskBox = TreeViewClass(self.__TaskFrame,
                                     columns = ('任务ID', '任务关键词', '任务链接', '删除任务', '任务状态'),
                                     show = 'headings',
                                     yscrollcommand = TaskScrollBar)


        # 整合两个列表
        self.NoteTab = ttk.Notebook(self.__ListFrame)
        self.NoteTab.pack(fill = 'both', expand = True)
        self.NoteTab.add(self.__SearchFrame, text = '搜索结果')
        self.NoteTab.add(self.__TaskFrame, text = '任务列表')

    def setupBottomPart(self):
        # 绘制爬取结果列表
        TaskScrollBar = ttk.Scrollbar(self.__resultFrame)
        TaskScrollBar.pack(side = "right", fill = "y")
        self.resultBox = TreeViewClass(self.__resultFrame,
                                       columns = ('任务ID', '任务关键词', '任务链接', '任务状态'),
                                       show = 'headings',
                                       yscrollcommand = TaskScrollBar
                                       )

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
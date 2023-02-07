import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import requests


class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.master = parent

    def setupFrame(self):

        self.__CommandFrame = ttk.LabelFrame(self, text = '控制台')
        self.__CommandFrame.grid(row = 0, column = 0, padx = (20, 10), pady = (20, 10))
        self.__ListFrame = ttk.LabelFrame(self, text = '商品列表')
        self.__ListFrame.grid(row = 0, column = 1, padx = (20, 10), pady = (20, 10))
        self.__TaskFrame = ttk.LabelFrame(self, text = '任务列表')
        self.__TaskFrame.grid(row = 0, column = 2, padx = (20, 10), pady = (20, 10))

        self.__resultFrame = ttk.LabelFrame()


    def setupTopPart(self):
        pass
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
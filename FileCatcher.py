import tkinter as tk
from tkinter import ttk
import os
import time
import requests as rq
from lxml import etree

class Application(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(row=0, column=0, padx=6, pady=6, sticky=tk.NSEW)
        self.create_widgets()

    def create_widgets(self):
        "创建组件"
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, weight=1)

        pageAddrText = ttk.Label(self, text="页面地址: ")
        pageAddrText.grid(row=0, column=0)

        self.pageUrl = ttk.Entry(self, width=45)
        self.pageUrl.grid(row=0, column=1, sticky=tk.E+tk.W)

        regExpText = ttk.Label(self, text="规则: ")
        regExpText.grid(row=0, column=2, padx=(10, 0))

        self.regExp = ttk.Entry(self, width=20)
        self.regExp.grid(row=0, column=3, sticky=tk.E+tk.W)

        goBtn = ttk.Button(self, width=6)
        goBtn["text"] = "Go"
        goBtn["command"] = self.get_download_list
        goBtn.grid(row=0, column=4, padx=(10, 0))

        self.table = ttk.Treeview(self, show="headings")
        self.table["columns"] = ("id", "name")
        self.table.column("id", width=36, anchor="center")
        self.table.column("name", width=460, anchor="w")
        self.table.heading("id", text="№")
        self.table.heading("name", text="文件名称")
        self.table.bind("<Button-3>", self.popup_download_menu)
        self.table.grid(row=1, column=0, columnspan=5, pady=(10, 0), sticky=tk.NSEW)

        tableScroll = tk.Scrollbar(self, orient="vertical", command=self.table.yview)
        tableScroll.grid(row=1, column=4, padx=1, pady=(11, 1), sticky=tk.N+tk.S+tk.E)
        self.table.configure(yscrollcommand=tableScroll.set)

        self.downloadMenu = tk.Menu(self, tearoff=0)
        self.downloadMenu.add_command(label="下载选中的文件", command=self.download_some)
        self.downloadMenu.add_separator()
        self.downloadMenu.add_command(label="下载全部文件", command=self.download_all)

    def get_download_list(self):
        "获取下载列表"
        # 解析文件下载地址
        text = rq.get(self.pageUrl.get()).text
        html = etree.HTML(text)
        self.downloadList = html.xpath(self.regExp.get())

        # 清空表格数据
        children = self.table.get_children()
        for item in children:
            self.table.delete(item)

        # 在表格插入数据
        id = 1
        for fileAddr in self.downloadList:
            self.table.insert("", "end", values=(id, os.path.basename(fileAddr.text)))
            id += 1

    def popup_download_menu(self, event):
        "弹出下载菜单"
        self.downloadMenu.post(event.x_root, event.y_root)

    def download_some(self):
        "下载选中的文件"
        for item in self.table.selection():
            itemVal = self.table.item(item, "values")
            n = 1
            for fileAddr in self.downloadList:
                if int(itemVal[0]) == n:
                    os.popen("start Thunder {url}".format(url=fileAddr.text))
                    time.sleep(4)
                n += 1

    def download_all(self):
        "下载全部文件"
        for fileAddr in self.downloadList:
            os.popen("start Thunder {url}".format(url=fileAddr.text))
            time.sleep(4)

os.popen("start Thunder")
time.sleep(6)

window = tk.Tk()
window.iconbitmap("icon/FileCatcher.ico")
window.title("FileCatcher")
window.geometry("600x400")
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)

app = Application(master=window)
app.mainloop()
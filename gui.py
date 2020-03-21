#!/usr/bin/env python3
from tkinter import Tk, W, E, N, S, Text, StringVar, Entry, scrolledtext, Scrollbar
from tkinter import ttk
from tkinter import filedialog
import flasher



class GUIForBootloader(Tk):
    def __init__(self):
        super(GUIForBootloader, self).__init__()
        self.title("Stm32F4 Flash Loader")
        self.geometry("400x400")
        self.resizable(False, False)
        self.wm_iconbitmap('µc.ico')
        self.guiInit()



    def guiInit(self):

        for row in range(6):
            self.rowconfigure(row, weight=0)
        for column in range(2):
            self.columnconfigure(column, weight=2)

        self.filePathOutput = StringVar()

        #Label widget
        self.label1 = ttk.Label(text="Com Port :")
        self.label1.grid(row=0, column=0, sticky=W)

        self.label2 = ttk.Label(text="Baud Rate :")
        self.label2.grid(row=2, column=0, sticky=W)

        self.label3 = ttk.Label(text="Bootloader Commands :")
        self.label3.grid(row=0, column=2, sticky=E)

        self.label4= ttk.Label(text="Path File :")
        self.label4.grid(row=4, column=0, sticky=W)

        self.label4 = ttk.Label(text=" Console Output :")
        self.label4.grid(row=8, column=0, sticky=W)

        # Combobox widget
        self.ComboBox1 = ttk.Combobox(self, width=15)
        self.ComboBox1['values'] = ("COM1", "COM2", "COM3", "COM4")
        self.ComboBox1.grid(row=1, column=0)

        self.ComboBox2 = ttk.Combobox(self, width=25)
        self.ComboBox2['values'] = (
        "BL_GET_VER", "BL_GET_HELP", "BL_GET_CID", "BL_GET_RDP_STATUS", "BL_GO_TO_ADDR", "BL_FLASH_ERASE",
        "BL_MEM_WRITE", "BL_EN_R_W_PROTECT", "BL_MEM_READ", "BL_OTP_READ", "BL_DIS_R_W_PROTECT",
        "BL_READ_SECTOR_P_STATUS")
        self.ComboBox2.grid(row=1, column=2)

        self.ComboBox3 = ttk.Combobox(self, width=15)
        self.ComboBox3['values'] = (
        "110 ", "300", "600 ", "1200", "2400 ", "4800", "9600 ", "19200", "38400 ", "57600", "115200 ", "230400",
        "460000 ", "921600", "1843200 ", "3686400")
        self.ComboBox3.grid(row=3, column=0)

        # Button widget
        self.Button1 = ttk.Button(text="Send Commands")
        self.Button1.grid(row=3, column=2, sticky=E)

        self.Button2 = ttk.Button(text="Test Connection")
        self.Button2.grid(row=3, column=1, sticky=W)

        self.Button3 = ttk.Button(text="Browse File", command=self.GetFileCallBack)
        self.Button3.grid(row=5, column=2, sticky=E)

        self.Button4 = ttk.Button(text="Start Flash")
        self.Button4.grid(row=7, column=2, sticky=E)

        #Entery widget
        self.entry1 = ttk.Entry(self, width='100', textvariable=self.filePathOutput).grid(row=5, column=0, columnspan=2)

        # Progressbar widget
        self.Progressbar1 = ttk.Progressbar(self, length=400, mode='determinate')
        self.Progressbar1.grid(row=7, column=0, columnspan=2)

        #scrolled text widget
        self.scroller1 = scrolledtext.ScrolledText(self, width=50, height=13)
        self.scroller1.grid(column=0, columnspan=3)


    def GetFileCallBack(self):
        self.filename = filedialog.askopenfilename(initialdir="C:/", title="Select File", filetypes=[("binary file", "*.hex")])
        self.filePathOutput.set(self.filename)


if __name__=='__main__':
    gui = GUIForBootloader()
    gui.mainloop()

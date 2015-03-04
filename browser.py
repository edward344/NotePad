#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Tkinter import *
import tkMessageBox
import os,sys
from os import path 

class Browser(object):
    def __init__(self,app,command_name):
        self.top = Toplevel()
        self.top.title(command_name)
        self.top.geometry("320x240")
        
        self.directory = self.get_dir()
        
        self.frame1 = Frame(self.top)
        scrollbar = Scrollbar(self.frame1)
        self.listbox = Listbox(self.frame1,yscrollcommand=scrollbar.set,width="45")
        scrollbar.config(command=self.listbox.yview)
        scrollbar.pack(side=RIGHT,fill=Y)
        self.listbox.pack(side=LEFT,fill=BOTH,expand=1)
        
        self.items = []
        for item in self.get_files():
            self.listbox.insert(END,item)
            
        self.frame2 = Frame(self.top)
        btn_back = Button(self.frame2,text="<-",command=self.back)
        btn_back.pack(side=LEFT)
        btn_open = Button(self.frame2,text=command_name,command=self.command_callback)
        btn_open.pack(side=LEFT)
        btn_cancel = Button(self.frame2,text="Cancel",command=self.top.destroy)
        btn_cancel.pack(side=LEFT)
        
        self.app = app
        
    def pack(self):
        self.frame1.pack()
        self.frame2.pack()
        
    def get_dir(self):
        s = os.getcwd()
        if sys.platform == "win32":
            s = s.replace("\\","/")
        return s

    def get_files(self):
        file_list = []
        try:
            if sys.platform == "win32":
                for item in os.listdir(self.directory + "/"):
                    if path.isdir(self.directory + "/" + item):
                        file_list.append(item + "   <DIR>")
                        self.items.append(item)
                    elif item[-4:] == ".txt":
                        file_list.append(item)
                        self.items.append(item)
            else:
                for item in os.listdir(self.directory + "/"):
                    if path.isdir(self.directory + "/" + item):
                        file_list.append(item + "   <DIR>")
                        self.items.append(item)
                    else:
                        file_list.append(item)
                        self.items.append(item)
        except WindowsError:
            tkMessageBox.showwarning("Open Directory","Could not open the directory...")
            self.top.destroy()
        return file_list

        
    def get_filename(self):
        t = self.listbox.curselection()
        if len(t) > 0:
            if path.isdir(self.directory + "/" + self.items[t[0]]):
                self.directory = self.directory + "/" + self.items[t[0]]
                self.listbox.delete(0,END)
                self.items = []
                for item in self.get_files():
                    self.listbox.insert(END,item)
                return "Directory"
            else:
                return self.directory + "/" + self.items[t[0]]
        else:
            return "None"
    
    def back(self):
        if self.directory.count("/") > 2:
            self.directory = self.directory[:self.directory.rfind("/")]
            self.listbox.delete(0,END)
            self.items = []
            for item in self.get_files():
                self.listbox.insert(END,item)

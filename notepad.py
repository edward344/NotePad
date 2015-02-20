#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
import tkMessageBox
import os,sys

class Open_file(object):
    def __init__(self,app):
        self.top = Toplevel()
        self.top.title("Open")
        label = Label(self.top,text="Enter the file to open:")
        label.pack()
        self.entry = Entry(self.top,width=60)
        self.entry.insert(END,self.get_dir() + "/")
        self.entry.pack()
            
        frame = Frame(self.top)
        btn_open = Button(frame,text="Open",command=self.open_file)
        btn_open.pack(side=LEFT)
        btn_cancel = Button(frame,text="Cancel",command=self.top.destroy)
        btn_cancel.pack(side=LEFT)
        frame.pack()
        
        self.app = app
        
    def get_dir(self):
        s = os.getcwd()
        if sys.platform == "win32":
            s = s.replace("\\","/")
        return s
        
    def open_file(self):
        self.app.text.delete("1.0",END)
        name = self.entry.get()
        if sys.platform == "win32":
            if name[-4:] == ".txt":
                try:
                    f = open(name)
                    
                    for line in f:
                        self.app.text.insert(END,line)
                    
                    f.close()
                    
                    self.app.new_file = False
                    self.app.file_name = name
                    self.app.master.title(name[name.rfind("/")+1:] + ": NotePad")
                    self.app.changed = False
                except IOError:
                    tkMessageBox.showwarning("Open file","Cannot open this file...")
                
            else:
                tkMessageBox.showwarning("Open file","Cannot open this file...")
        else:
            try:
                f = open(name)
                
                for line in f:
                    self.app.text.insert(END,line)
                    
                f.close()
                    
                self.app.new_file = False
                self.app.file_name = name
                self.app.master.title(name[name.rfind("/")+1:] + ": NotePad")
                self.app.changed = False
            except IOError:
                tkMessageBox.showwarning("Open file","Cannot open this file...")
            
        self.top.destroy()
        
class Save_file(object):
    def __init__(self,app):
        self.top = Toplevel()
        self.top.title("Save as")
        label = Label(self.top,text="Enter the name of the file to save")
        label.pack()
        self.entry = Entry(self.top,width=60)
        self.entry.insert(END,self.get_dir() + "/")
        self.entry.pack()
        
        frame = Frame(self.top)
        btn_open = Button(frame,text="Save",command=self.save_file)
        btn_open.pack(side=LEFT)
        btn_cancel = Button(frame,text="Cancel",command=self.top.destroy)
        btn_cancel.pack(side=LEFT)
        frame.pack()
        
        self.app = app
        
    def save_file(self):
        name = self.entry.get()
        if name[-1] != "/":
            if name[-4:] != ".txt" and sys.platform == "win32":
                name += ".txt"
            
            f = open(name,"w")
            text = self.app.text.get("1.0",END).encode("utf-8")
            f.write(text)
            f.close()
            self.app.file_name = name
            self.app.master.title(name[name.rfind("/")+1:] + ": NotePad")
            self.app.new_file = False
            self.app.changed = False
            
        else:
            tkMessageBox.showwarning("Save file","You have to name the file...")
        self.top.destroy()
        
    def get_dir(self):
        s = os.getcwd()
        if sys.platform == "win32":
            s = s.replace("\\","/")
        return s
        

class App(object):
    file_name = "Untitled"
    changed = False
    def __init__(self,master):
        self.master = master
        master.title("Untitled: NotePad")
        master.geometry("640x480")
        # add a menu:
        menubar = Menu(master)
        filemenu = Menu(menubar,tearoff=0)
        filemenu.add_command(label="New",command=self.new_file_menu)
        filemenu.add_command(label="Open",command=self.open_file_menu)
        filemenu.add_command(label="Save",command=self.save_file_menu)
        filemenu.add_command(label="Save as",command=self.save_as_file_menu)
        filemenu.add_command(label="Exit",command=self.exit_menu)
        menubar.add_cascade(label="File",menu=filemenu)
        
        editmenu = Menu(menubar,tearoff=0)
        editmenu.add_command(label="Cut",command=self.cut)
        editmenu.add_command(label="Copy",command=self.copy)
        editmenu.add_command(label="Paste",command=self.paste)
        menubar.add_cascade(label="Edit",menu=editmenu)

        
        master.config(menu=menubar)
        
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)
        
        self.text = Text(master,yscrollcommand=scrollbar.set)
        self.text.bind("<Button-3>",self.popmenu)
        self.text.pack(side=LEFT,fill=BOTH,expand=1)
        scrollbar.config(command=self.text.yview)
        
        self.text.bind("<Key>",self.key_callback)
        
        master.protocol("WM_DELETE_WINDOW",self.close_window)
        
    def close_window(self):
        if self.changed:
            if tkMessageBox.askyesno("Quit","do you want to save the file..."):
                if self.file_name == "Untitled":
                    obj = Save_file(self)
                else:
                    f = open(self.file_name,"w")
                    text = self.text.get("1.0",END).encode("utf-8")
                    f.write(text)
                    f.close()
                    self.master.destroy()
            else:
                self.master.destroy()
        else:
            self.master.destroy()
        
    def key_callback(self,event):
        if not self.changed:
            self.master.title("*" + self.file_name[self.file_name.rfind("/")+1:] + ": NotePad")
            self.changed = True
        
    def popmenu(self,event):
        menu = Menu(self.master,tearoff=0)
        menu.add_command(label="Cut",command=self.cut)
        menu.add_command(label="Copy",command=self.copy)
        menu.add_command(label="Paste",command=self.paste)
        menu.post(event.x_root,event.y_root)

        
    def cut(self):
        try:
            self.copy()
            self.text.delete("sel.first","sel.last")
            self.master.title("*" + self.file_name[self.file_name.rfind("/")+1:] + ": NotePad")
            self.changed = True
        except TclError:
            pass
        
    def copy(self):
        try:
            self.text.clipboard_clear()
            text = self.text.get("sel.first","sel.last")
            self.text.clipboard_append(text)
        except TclError:
            pass
                
    def paste(self):
        try:
            text = self.text.selection_get(selection="CLIPBOARD")
            self.text.insert(INSERT,text)
            self.master.title("*" + self.file_name[self.file_name.rfind("/")+1:] + ": NotePad")
            self.changed = True
        except TclError:
            pass
            
        
    def open_file_menu(self):
        obj = Open_file(self)
        
    def save_as_file_menu(self):
        obj = Save_file(self)
        
    def save_file_menu(self):
        if self.file_name == "Untitled":
            obj = Save_file(self)
        else:
            f = open(self.file_name,"w")
            text = self.text.get("1.0",END).encode("utf-8")
            f.write(text)
            f.close()
            self.changed = False
            self.master.title(self.file_name[self.file_name.rfind("/")+1:] + ": NotePad")

    def new_file_menu(self):
        self.text.delete("1.0",END)
        self.file_name = "Untitled"
        self.master.title("Untitled: NotePad")
        self.changed = False
        
    def exit_menu(self):
        if self.changed:
            if tkMessageBox.askyesno("Quit","do you want to save the file..."):
                if self.file_name == "Untitled":
                    obj = Save_file(self)
                else:
                    f = open(self.file_name,"w")
                    text = self.text.get("1.0",END).encode("utf-8")
                    f.write(text)
                    f.close()
                    self.master.destroy()
            else:
                self.master.destroy()
        else:
            self.master.destroy()


def main():
    root = Tk()
    app = App(root)
    root.mainloop()

if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
import tkMessageBox
import os,sys
from browser import Browser

class Open_File(Browser):
    def __init__(self,app,command_name):
        Browser.__init__(self,app,command_name)
        label = Label(self.top,text="Select the file/directory you want to open:")
        label.pack()
        self.pack()
        
    def command_callback(self):
        filename = self.get_filename()
        if sys.platform == "win32":
            if filename == "None":
                tkMessageBox.showwarning("Open file","Please Select a file...")
            elif filename[-4:] == ".txt":
                self.app.text.delete("1.0",END)
                try:
                    f = open(filename)
                    
                    for line in f:
                        self.app.text.insert(END,line)
                    
                    f.close()
                
                    self.app.new_file = False
                    self.app.file_name = filename
                    self.app.master.title(filename[filename.rfind("/")+1:] + ": NotePad")
                    self.app.changed = False
                except IOError:
                    tkMessageBox.showwarning("Open file","Cannot open this file...")
                self.top.destroy() # kill the window...    
        else:
            if filename == "None":
                tkMessageBox.showwarning("Open file","Please Select a file...")
            elif filename != "Directory":
                self.app.text.delete("1.0",END)
                try:
                    f = open(filename)
                    
                    for line in f:
                        self.app.text.insert(END,line)
                    
                    f.close()
                
                    self.app.new_file = False
                    self.app.file_name = filename
                    self.app.master.title(filename[filename.rfind("/")+1:] + ": NotePad")
                    self.app.changed = False
                except IOError:
                    tkMessageBox.showwarning("Open file","Cannot open this file...")
                self.top.destroy() # kill the window... 
                
class Save_File(Browser):
    def __init__(self,app,command_name):
        Browser.__init__(self,app,command_name)
        label = Label(self.top,text="Enter the name of your file...")
        label.pack()
        self.entry = Entry(self.top,width=30)
        self.entry.pack()
        self.pack()
        
    def command_callback(self):
        if self.get_filename() != "Directory":
            if len(self.entry.get()) > 0:
                filename = self.directory + "/" + self.entry.get()
                if filename[-4:] != ".txt" and sys.platform == "win32":
                    filename += ".txt"
                
                f = open(filename,"w")
                text = self.app.text.get("1.0",END).encode("utf-8")
                f.write(text)
                f.close()
                self.app.file_name = filename
                self.app.master.title(filename[filename.rfind("/")+1:] + ": NotePad")
                self.app.new_file = False
                self.app.changed = False
                self.top.destroy() #kill the window...
            else:
                tkMessageBox.showwarning("Save file","You have to name the file...")
            

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
                    obj = Save_File(self,"Save as")
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
            
    #----------File menu commands:--------------------------------------
        
    def open_file_menu(self):
        if self.changed:
            if tkMessageBox.askyesno("Quit","do you want to save the file..."):
                if self.file_name == "Untitled":
                    obj = Save_File(self,"Save as")
                else:
                    f = open(self.file_name,"w")
                    text = self.text.get("1.0",END).encode("utf-8")
                    f.write(text)
                    f.close()
                    #---------------------------------------------------
            self.text.delete("1.0",END)
            self.file_name = "Untitled"
            self.master.title("Untitled: NotePad")
            self.changed = False
        obj = Open_File(self,"Open")

    def save_as_file_menu(self):
        obj = Save_File(self,"Save")

   #--------------------------------------------------------------------     
        
    def save_file_menu(self):
        if self.file_name == "Untitled":
            obj = Save_File(self,"Save as")
        else:
            f = open(self.file_name,"w")
            text = self.text.get("1.0",END).encode("utf-8")
            f.write(text)
            f.close()
            self.changed = False
            self.master.title(self.file_name[self.file_name.rfind("/")+1:] + ": NotePad")

    def new_file_menu(self):
        if self.changed:
            if tkMessageBox.askyesno("New","Do you want to save the file..."):
                if self.file_name == "Untitled":
                    obj = Save_File(self,"Save as")
                else:
                    f = open(self.file_name,"w")
                    text = self.text.get("1.0",END).encode("utf-8")
                    f.write(text)
                    f.close()
        self.text.delete("1.0",END)
        self.file_name = "Untitled"
        self.master.title("Untitled: NotePad")
        self.changed = False
        
    def exit_menu(self):
        if self.changed:
            if tkMessageBox.askyesno("Quit","do you want to save the file..."):
                if self.file_name == "Untitled":
                    obj = Save_File(self,"Save as")
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

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is a simple Text Editor written in python using the Tkinter library.
************************************************************************
Author: Eduardo Alejandro Grando.									   *
e-mail: grandoeduardo64@gmail.com									   *
License: GPL v3														   *
************************************************************************
"""
from Tkinter import *
import tkMessageBox
import os,sys,sqlite3
from tkFileDialog import *
#=======================================================================
class FontStlye(object):
    def __init__(self,app):
        self.top = Toplevel()
        self.top.title("Font Style")
        #---------------------------------------------------------------
        label = Label(self.top,text="Please select a font style...",width=30)
        label.pack()
        #---------------------------------------------------------------
        styles = (
                "normal",
                "bold",
                "italic")
        #---------------------------------------------------------------
        for style in styles:
            Radiobutton(self.top,text=style,variable=app.style,value=style).pack(anchor=W)
        #---------------------------------------------------------------
        frame = Frame(self.top)
        frame.pack()
        applyButton = Button(frame,text="Apply",command=self.applyfontstyle)
        applyButton.pack(side=LEFT)
        acceptButton = Button(frame,text="Accept",command=self.applyfontstyle_exit)
        acceptButton.pack(side=RIGHT)
        #---------------------------------------------------------------
        self.app = app
        
    def applyfontstyle(self):
        self.app.fontstyle = self.app.style.get()
        self.app.text.config(font=(self.app.font,self.app.fontsize,self.app.fontstyle))
        
    def applyfontstyle_exit(self):
        self.app.fontstyle = self.app.style.get()
        self.app.text.config(font=(self.app.font,self.app.fontsize,self.app.fontstyle))
        self.top.destroy()
#=======================================================================
class FontType(object):
    def __init__(self,app):
        self.top = Toplevel()
        self.top.title("Font")
        #---------------------------------------------------------------
        label = Label(self.top,text="Please select a font...",width=30)
        label.pack()
        #---------------------------------------------------------------
        fonts = (
                "Arial",
                "Courier New",
                "Verdana",
                "Times New Roman",
                "Comic Sans MS",
                "Fixedsys",
                "MS Sans Serif",
                "MS Serif",
                "Symbol",
                "System")
        #---------------------------------------------------------------
        for font in fonts:
            Radiobutton(self.top,text=font,variable=app.fontvar,value=font).pack(anchor=W)
        #---------------------------------------------------------------
        frame = Frame(self.top)
        frame.pack()
        applyButton = Button(frame,text="Apply",command=self.applyfont)
        applyButton.pack(side=LEFT)
        acceptButton = Button(frame,text="Accept",command=self.applyfont_exit)
        acceptButton.pack(side=RIGHT)
        #---------------------------------------------------------------
        self.app = app
        
    def applyfont(self):
        self.app.font = self.app.fontvar.get()
        self.app.text.config(font=(self.app.font,self.app.fontsize,self.app.fontstyle))
        
    def applyfont_exit(self):
        self.app.font = self.app.fontvar.get()
        self.app.text.config(font=(self.app.font,self.app.fontsize,self.app.fontstyle))
        self.top.destroy()
#=======================================================================
class FontSize(object):
    def __init__(self,app):
        self.top = Toplevel()
        self.top.title("Font Size")
        #---------------------------------------------------------------
        label = Label(self.top,text="Please select a font size...",width=30)
        label.pack()
        #---------------------------------------------------------------
        self.scale = Scale(self.top,from_=10,to=25,orient=HORIZONTAL)
        self.scale.pack()
        self.scale.set(app.fontsize)
        #---------------------------------------------------------------
        frame = Frame(self.top)
        frame.pack()
        applyButton = Button(frame,text="Apply",command=self.applyfontsize)
        applyButton.pack(side=LEFT)
        acceptButton = Button(frame,text="Accept",command=self.applyfontsize_exit)
        acceptButton.pack(side=RIGHT)
        #---------------------------------------------------------------
        self.app = app
        
    def applyfontsize(self):
        self.app.fontsize = self.scale.get() 
        self.app.text.config(font=(self.app.font,self.app.fontsize,self.app.fontstyle))
    
    def applyfontsize_exit(self):
        self.app.fontsize = self.scale.get() 
        self.app.text.config(font=(self.app.font,self.app.fontsize,self.app.fontstyle))
        self.top.destroy()
#=======================================================================
#++++++++++++++++++++Main Class+++++++++++++++++++++++++++++++++++++++++
class App(object):
    file_name = "Untitled"
    changed = False
    fontsize = 12 #Hold the font size;
    font = "Courier New" #Hold the font;
    fontstyle = "normal" #hold the font style;
    def __init__(self,master):
        self.master = master
        master.title("Untitled: NotePad")
        master.geometry("640x480")
        
        #--Execute SQLite to retrieve the previous font, fontsize and fontstyle:
        self.retrieve_data()
        #---------------------------------------------------------------
        # add a menu: ..................................................
        menubar = Menu(master)
        filemenu = Menu(menubar,tearoff=0)
        filemenu.add_command(label="New",command=self.new_file)
        filemenu.add_command(label="Open",command=self.open_file)
        filemenu.add_command(label="Save",command=self.save_file)
        filemenu.add_command(label="Save as",command=self.save_as_file)
        filemenu.add_command(label="Exit",command=self.exit_menu)
        menubar.add_cascade(label="File",menu=filemenu)
        #---------------------------------------------------------------
        editmenu = Menu(menubar,tearoff=0)
        editmenu.add_command(label="Cut",command=self.cut)
        editmenu.add_command(label="Copy",command=self.copy)
        editmenu.add_command(label="Paste",command=self.paste)
        menubar.add_cascade(label="Edit",menu=editmenu)
        #---------------------------------------------------------------
        optionmenu = Menu(menubar,tearoff=0)
        optionmenu.add_command(label="Font",command=self.changefont)
        optionmenu.add_command(label="Font Size",command=self.changefontsize)
        optionmenu.add_command(label="Font Style",command=self.changefontstyle)
        menubar.add_cascade(label="Options",menu=optionmenu)
        #---------------------------------------------------------------
        master.config(menu=menubar)
        #---------------------------------------------------------------
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)
        #---------------------------------------------------------------
        self.text = Text(master,yscrollcommand=scrollbar.set)
        self.text.bind("<Button-3>",self.popmenu)
        self.text.pack(side=LEFT,fill=BOTH,expand=1)
        scrollbar.config(command=self.text.yview)
        #---------------------------------------------------------------
        self.text.bind("<Key>",self.key_callback)
        #~ self.text.bind("<Return>",self.return_key)
        #---------------------------------------------------------------
        master.protocol("WM_DELETE_WINDOW",self.close_window)
        #---------------------------------------------------------------
        #...............................................................
        if len(sys.argv) > 1:
            if sys.platform == "win32":
                if sys.argv[1][-4:] == ".txt":
                    try:
                        f = open(sys.argv[1])
                        for line in f:
                            self.text.insert(END,line)
                        f.close()
                        self.file_name = sys.argv[1]
                        self.master.title(self.file_name[self.file_name.rfind("/")+1:] + ": NotePad")
                        self.changed = False
                    except IOError:
                        tkMessageBox.showwarning("Open file","Cannot open this file...")
            else:
                try:
                    f = open(sys.argv[1])
                    for line in f:
                        self.text.insert(END,line)
                    f.close()
                    self.file_name = sys.argv[1]
                    self.master.title(self.file_name[self.file_name.rfind("/")+1:] + ": NotePad")
                    self.changed = False
                except IOError:
                    tkMessageBox.showwarning("Open file","Cannot open this file...")
        #---------------------------------------------------------------
        self.fontvar = StringVar() #hold the variable for radiobutton.
        self.fontvar.set(self.font)
        #---------------------------------------------------------------
        self.style = StringVar() #Hold the style variable for radiobutton
        self.style.set(self.fontstyle)
        # Set the font, font size and font style: ----------------------
        self.text.config(font=(self.font,self.fontsize,self.fontstyle))

	#===================================================================
	
    # Retrieve data from a database: -----------------------------------
    def retrieve_data(self):
        try:
            connection = sqlite3.connect("config.db")
            cursor = connection.cursor()    

            cursor.execute("SELECT font FROM info")
            self.font = str(cursor.fetchone()[0])
            
            cursor.execute("SELECT size FROM info")
            self.fontsize = cursor.fetchone()[0]
            
            cursor.execute("SELECT style FROM info")
            self.fontstyle = str(cursor.fetchone()[0])
            
            connection.close()
        except sqlite3.OperationalError:
            #if the database does not exist we create a new one:
            connection = sqlite3.connect("config.db")
            cursor = connection.cursor()
            cursor.execute("""
                            CREATE TABLE IF NOT EXISTS info (id INTEGER PRIMARY KEY NOT NULL,
                            font TEXT NOT NULL, size INTEGER NOT NULL,style TEXT NOT NULL)
                            """)
                    
            #connection.commit()
            cursor.execute("""
                            INSERT INTO info VALUES (1,'Courier New',12,'normal')
                            """)
            connection.commit()
            connection.close()
        
    # Update data to the database: -------------------------------------
    def update_data(self):
        # Store the font, fontsize and fontstyle in a database:
        commit = False
        connection = sqlite3.connect("config.db")
        cursor = connection.cursor()
            
        cursor.execute("SELECT font FROM info")
        if self.font != str(cursor.fetchone()[0]):
            cursor.execute("UPDATE info SET font = ? WHERE id = 1",(self.font,))
            commit = True
                
        cursor.execute("SELECT size FROM info")
        if self.fontsize != cursor.fetchone()[0]:
            cursor.execute("UPDATE info SET size = ? WHERE id = 1",(self.fontsize,))
            commit = True
            
        cursor.execute("SELECT style FROM info")
        if self.fontsize != str(cursor.fetchone()[0]):
            cursor.execute("UPDATE info SET style = ? WHERE id = 1",(self.fontstyle,))
            commit = True
            
        if commit:
            connection.commit()
        connection.close()
        
    # Option Menu ------------------------------------------------------
    def changefontsize(self):
        obj = FontSize(self)
        
    def changefont(self):
        obj = FontType(self)
        
    def changefontstyle(self):
        obj = FontStlye(self)
    #...................................................................
    def open_file(self):
        filename = str(askopenfilename(title="Open File",filetypes=[('text file','.txt')]))
        if len(filename) > 0:
            self.text.delete("1.0",END)
            try:
                f = open(filename)
                for line in f:
                    self.text.insert(END,line)
                f.close()
                self.file_name = filename
                self.master.title(filename[filename.rfind("/")+1:] + ": NotePad")
                self.changed = False
            except IOError:
                tkMessageBox.showwarning("Open file","Cannot open this file...") 
                
    def save_file(self):
        if self.file_name == "Untitled":
            self.save_as_file()
        else:
            f = open(self.file_name,"w")
            text = self.text.get("1.0",END).encode("utf-8")
            f.write(text)
            f.close()
            self.changed = False   
            self.master.title(self.file_name[self.file_name.rfind("/")+1:] + ": NotePad")
    
    def save_as_file(self):
        filename = str(asksaveasfilename(title="Save as File",defaultextension=".txt",filetypes=[('text file','.txt')]))
        if len(filename) > 0:
            f = open(filename,"w")
            text = self.text.get("1.0",END).encode("utf-8")
            f.write(text)
            f.close()
            self.file_name = filename
            self.master.title(filename[filename.rfind("/")+1:] + ": NotePad")
            self.changed = False
        
    def close_window(self):
        self.update_data()
        if self.changed:
            if tkMessageBox.askyesno("Quit","do you want to save the file..."):
                if self.file_name == "Untitled":
                    self.save_as_file()
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

    def new_file(self):
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
        self.update_data()
        if self.changed:
            if tkMessageBox.askyesno("Quit","do you want to save the file..."):
                if self.file_name == "Untitled":
                    self.save_as_file()
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
#=======================================================================

def main():
    root = Tk()
    app = App(root)
    root.mainloop()

if __name__ == '__main__':
    main()

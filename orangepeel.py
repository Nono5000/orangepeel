from tkinter import filedialog, colorchooser
from tkinter import *
import tkinter as tk
import tkinter.messagebox
import webbrowser
import os
from bs4 import BeautifulSoup
root = Tk()
root.geometry('500x600+200+150')
root.title("Orangepeel")
scroll = Scrollbar(root)
text=Text(root, width = 500, height = 700, fg = 'orange', yscrollcommand = scroll.set )
doctype = '<!DOCTYPE html>'
text.insert(tk.INSERT, doctype)
def savef():
    while True:
        try:
            contents = text.get("1.0", "end-1c")
            file = open(filename, "w")
            file.write(contents)
            file.close()
        except NameError:
            saveasf()
def aboutcomm():
    tk.messagebox.showinfo(title = "About", message = "Orangepeel is a python based HTML editor/IDE.")   
def warningopen():
        tk.messagebox.showwarning(title = 'Are you sure ?', message = 'If you open a document without saving this one first, you will lose all of your data in the current document !')
def openfile():
    try:
        warningopen()
        global filename
        filename = filedialog.askopenfilename(initialdir = "/home/pi", title = "Open file", filetypes = (("HTML files", "*.html"),("XML files", "*.xml"), ("text files", "*.txt"),("all files", "*.*")))
        file = open(filename, "r")
        filecontents=file.read()
        text.delete("1.0", "end")
        text.insert(tk.INSERT, filecontents)
    except UnicodeDecodeError:
        tk.messagebox.showerror(title = 'Can\'t decode', message = 'Invalid file encoding')
def saveasf():
    global saveloc
    contents = text.get("1.0", "end-1c")
    saveloc=filedialog.asksaveasfilename()
    file = open(saveloc, "w")
    file.write(contents)
    file.close()
def newf():
    warningopen()
    savef()
    text.delete("1.0", "end")
def copy():
    global clipboard
    selec = text.selection_get()
    clipboard = selec
def cut():
    selec = text.selection_get()
    clipboard=selec
    text.delete("selection_get()")
def paste():
    text.insert(INSERT, clipboard)
def previewinbrowser():
    try:
        webbrowser.open('file://' + filename)
    except NameError:
        tk.messagebox.showerror(title = 'Preview in browser', message = 'Save this document before previewing it in browser.')
        savef()
def notags():
    htmltags = text.get('1.0', 'end')
    soup = BeautifulSoup(htmltags, "html.parser") # create a new bs4 object from the html data loaded
    for script in soup(["script", "style"]): # remove all javascript and stylesheet code
            script.extract()
    # get text
    htmlnotags = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in htmlnotags.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    htmlnotags = '\n'.join(chunk for chunk in chunks if chunk)
    txtsaveloc=filedialog.asksaveasfilename()
    f = open(txtsaveloc, mode = 'w')
    f.write(htmlnotags)
    f.close()
def red():
    text.config(fg = 'red')
def orange():
    text.config(fg = 'orange')
def yellow():
    text.config(fg = 'yellow')
def green():
    text.config(fg = 'green')
def blue():
    text.config(fg = 'blue')
def purple():
    text.config(fg = 'purple')
def brown():
    text.config(fg = 'brown')
def black():
    text.config(fg = 'black')
def colorpick():
    colorchooser.askcolor()
menu = Menu(root)
file = Menu(menu, tearoff = 0, font = ('courier'))
edit = Menu(menu, tearoff = 0, font = ('courier'))
help = Menu(menu, tearoff = 0, font = ('courier'))
tools = Menu(menu, tearoff = 0, font = ('courier'))
textpref = Menu(menu, tearoff = 0, font = ('courier'))

web = Button(root, text = 'preview in browser', font = ('courier', '12'), command = previewinbrowser, fg = 'blue')
tags2txt = Button(root, text = 'export as plain text', font = ('courier', '12'), command = notags, fg = 'red')
menu.add_cascade(label = "File", menu=file, font = ('courier'))
file.add_command(label="New", command=newf)
file.add_command(label="Open", command=openfile)
file.add_command(label="Save as", command=saveasf)
file.add_command(label="Save", command=savef)
file.add_command(label="Quit", command=quit)
menu.add_cascade(label="Edit", menu=edit, font = ('courier'))
edit.add_command(label="Cut", accelerator="Ctrl+X", command=cut)
edit.add_command(label="Copy", accelerator="Ctrl+C", command=copy)
edit.add_command(label="Paste", accelerator="Ctrl+V", command=paste)
menu.add_cascade(label = "Help", menu = help, font = ('courier'))
help.add_command(label="About", command=aboutcomm)
menu.add_cascade(label = 'Text preferences', menu = textpref, font = ('courier'))
textpref.add_command(label = 'Red', command = red)
textpref.add_command(label = 'Orange', command = orange)
textpref.add_command(label = 'Yellow', command = yellow)
textpref.add_command(label = 'Green', command = green)
textpref.add_command(label = 'Blue', command = blue)
textpref.add_command(label = 'Purple', command = purple)
textpref.add_command(label = 'Brown', command = brown)
textpref.add_command(label = 'Black', command = black)
menu.add_cascade(label = 'Tools', menu = tools, font = ('courier'))
tools.add_command(label="color picker", command = colorpick)

scroll.pack(side = 'right', fill = 'y')
scroll.config( command = text.yview )  

web.pack(fill = 'x')
tags2txt.pack(fill = 'x')
text.pack()
root.config(menu=menu)
root.mainloop()

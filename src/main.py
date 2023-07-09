import os
import sys
import nbtlib
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.font import Font
import threading
from PIL import Image, ImageTk

# relative path stuffs
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

try:
    import iconpath
    path = 'src\\assets\\fave.ico'
except:
    path = 'assets\\fave.ico'

# Creating tkinter root
root = tk.Tk()
root.title('Inventory Salvage')
root.resizable(False, False)
im = Image.open(resource_path(path))
photo = ImageTk.PhotoImage(im)
root.wm_iconphoto(True, photo)
WINDOW_HEIGHT = 350
WINDOW_WIDTH = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cordinate = int((screen_width/2) - (WINDOW_WIDTH/2))
y_cordinate = int((screen_height/2) - (WINDOW_HEIGHT/2))
root.geometry("{}x{}+{}+{}".format(WINDOW_WIDTH, WINDOW_HEIGHT, x_cordinate, y_cordinate))
PAD_X = 25
PAD_Y = 25

font = Font(family = 'Arial', size = 9, weight = 'normal')

# label text for title
ttk.Label(root, text = "Inventory Salvage - Copy from one player to another!", foreground ="black", font = font).grid(row = 0, column = 1, pady = 8)

# select tag to copy
ttk.Label(root, text = "Copy tag:", font = font).grid(column = 0, row = 5, padx = PAD_X, pady = PAD_Y)

extraspace = ' '*85
# old player file
ttk.Label(root, text = 'Old player: ', font = font).grid(column = 0, row = 7, padx = PAD_X, pady = PAD_Y)
oldplayer = tk.StringVar()
oldplayerDisplay = tk.StringVar()
oldplayerDisplay.set(extraspace)
ttk.Label(root, textvariable = oldplayerDisplay, font = font).grid(column = 1, row = 7, padx = 10, pady = 25)

# new player file
ttk.Label(root, text = 'New player: ', font = font).grid(column = 0, row = 9, padx = PAD_X, pady = PAD_Y)
newplayer = tk.StringVar()
newplayerDisplay = tk.StringVar()
newplayerDisplay.set(extraspace)
ttk.Label(root, textvariable = newplayerDisplay, font = font).grid(column = 1, row = 9, padx = 10, pady = 25)

# error msgs
errorMsg = tk.StringVar()
ttk.Label(root, textvariable = errorMsg, foreground = 'red', wraplength = 80, justify = 'left').grid(column = 0, row = 12, padx = 10, pady = 25)

# success msgs
successMsg = tk.StringVar()
ttk.Label(root, textvariable = successMsg, foreground = 'green', wraplength = 80, justify = 'left').grid(column = 1, row = 12, padx = 10, pady = 25)

# Combobox creation
n = tk.StringVar()
tagcombo = ttk.Combobox(root, width = 27, textvariable = n)


# Adding combobox drop down list
opts = [
	'EnderItems',
	'Inventory',
]
tagcombo['values'] = (opts)
tagcombo.grid(column = 1, row = 5)

def selectFile(label, labelDisplay):
	filename = askopenfilename()
	if '.dat' not in filename: return
	labelDisplay.set(filename.split('/')[-1])
	label.set(filename)

def copyOver():
    currentOpt = opts[current := tagcombo.current()]
    oldie, newbie = oldplayer.get(), newplayer.get()
    if current < 0: afterError('Selected tag is invalid! :C'); return
    if '.dat' not in oldie: afterError('Old player is invalid! :C'); return
    if '.dat' not in newbie: afterError('New player is invalid! :C'); return
    if oldie == newbie: afterError('Can\'t copy from the same file! :C'); return
    old = nbtlib.load(oldie)
    new = nbtlib.load(newbie)
    new[currentOpt] = old[currentOpt]
    try:
        new.save()
    except:
        afterError('something went wrong!')
    afterSuccess('Successfully copied data!'); return

def afterError(text):
    errorMsg.set(text)
    successMsg.set('')
    threading.Timer(function = lambda: errorMsg.set(''), interval = 3.0).start()

def afterSuccess(text):
    errorMsg.set('')
    successMsg.set(text)
    threading.Timer(function = lambda: successMsg.set(''), interval = 3.0).start()

# btns idk
ttk.Button(root, text = "Select File", command = lambda: selectFile(oldplayer, oldplayerDisplay)).grid(row = 7, column = 4)
ttk.Button(root, text = "Select File", command = lambda: selectFile(newplayer, newplayerDisplay)).grid(row = 9, column = 4)
ttk.Button(root, text = "Copy! :D", command = lambda: copyOver()).grid(row = 11, column = 4)


if __name__ == '__main__':
	root.mainloop()
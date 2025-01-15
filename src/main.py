import os
import sys
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.font import Font
from PIL import Image, ImageTk
from worlds import World
from logger import Logger
from combos import Combo
from info import openinfo
from math import floor, ceil

# relative path stuffs (do not touch please)
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

try:
    # development lol
    import iconpath
    fave_ico_path = 'src\\assets\\fave.ico'
    info_webp_path = 'src\\assets\\i_icon.webp'
    info_txt_path = 'src\\assets\\info.txt'
except:
    # production lol
    fave_ico_path = 'assets\\fave.ico'
    info_webp_path = 'assets\\i_icon.webp'
    info_txt_path = 'assets\\info.txt'

# generating tkinter root
root = tk.Tk()
root.title('Inventory Salvage')
root.resizable(False, False)
im = Image.open(resource_path(fave_ico_path))
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

# extra space for formatting (im too lazy to do it right so i kept the old code that did it)
ttk.Label(root, text = '', font = font).grid(column = 0, row = 7, padx = PAD_X, pady = PAD_Y)
ttk.Label(root, text = '', font = font).grid(column = 0, row = 9, padx = PAD_X, pady = PAD_Y)

savename = lambda s, t: f'Save {t}:\n{s}'
oldsave = tk.StringVar()
oldsave.set('Select save A')
newsave = tk.StringVar()
newsave.set('Select save B')

# Logger
# success msgs
successMsg = tk.StringVar()
ttk.Label(root, textvariable = successMsg, foreground = 'green', wraplength = 120, justify = 'left').grid(column = 1, row = 12, padx = 4, pady = 25)

# error msgs
errorMsg = tk.StringVar()
ttk.Label(root, textvariable = errorMsg, foreground = 'red', wraplength = 80, justify = 'left').grid(column = 0, row = 12, padx = 4, pady = 25)

logger = Logger(successMsg, errorMsg)
logger.afterSuccess('Welcome!')

# info button
image = Image.open(resource_path(info_webp_path))  # Replace with the path to your image file
image_resized = image.resize((16, 16))
photo = ImageTk.PhotoImage(image_resized)
info = tk.Button(root, image=photo, bd=0)  # 'bd=0' removes the border around the button
info.grid(column = 3, row = 0, padx = PAD_X, pady = PAD_Y)
info.config(command = lambda: openinfo(resource_path(info_txt_path), x_cordinate + floor(WINDOW_WIDTH/6), y_cordinate + floor(WINDOW_HEIGHT/6)))

# Combobox creation
n = tk.StringVar()
tagopts = [
	'EnderItems',
	'Inventory',
    'Pos',
    'Motion',
    'Rotation',
    'XpTotal',
    'Dimension',
    'Health',
    'playerGameType',
    'foodLevel',
]
tagopts.sort()
tagcombo = Combo(root, width = 27, textvariable = n, completevalues = tagopts)
tagcombo.grid(column = 1, row = 5)


def selectFile(label, labelDisplay):
	filename = askopenfilename()
	if filename: return
	labelDisplay.set(filename.split('/')[-1])
	label.set(filename)

def copyOver(A: World, B: World):
    currentOpt = tagopts[current := tagcombo.current()]
    if current < 0: logger.afterError('Selected tag is invalid! :C'); return
    if type(A.player) == type(None): logger.afterError('Old player is invalid! :C'); return
    if type(B.player) == type(None): logger.afterError('New player is invalid! :C'); return
    B.replace_prop(currentOpt, A.extract_prop(currentOpt))
    try:
        B.save()
        logger.afterSuccess('Successfully copied data!')
    except:
        logger.afterError('Something went wrong!')

# btns idk
oldbtn = ttk.Button(root, textvariable = oldsave)
oldbtn.grid(row = 7, column = 0)
newbtn = ttk.Button(root, textvariable = newsave)
newbtn.grid(row = 9, column = 0)
copybtn = ttk.Button(root, text = "Copy! :D", command = lambda: copyOver(world1, world2))
copybtn.grid(row = 11, column = 3)

# worlds
secondcombostr = tk.StringVar()
firstcombo = Combo(root, width = 27, textvariable = secondcombostr, state='disabled')
firstcombo.grid(row = 7, column = 1)
world1 = World(root, firstcombo, logger, lambda s: oldsave.set(savename(s, 'A')), oldbtn)

secondcombostr = tk.StringVar()
secondcombo = Combo(root, width = 27, textvariable = secondcombostr, state='disabled')
secondcombo.grid(row = 9, column = 1)
world2 = World(root, secondcombo, logger, lambda s: newsave.set(savename(s, 'B')), newbtn)

oldbtn.configure(command = lambda: world1.select_save())
newbtn.configure(command = lambda: world2.select_save())

if __name__ == '__main__':
	root.mainloop()
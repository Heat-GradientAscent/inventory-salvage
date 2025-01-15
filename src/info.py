import tkinter as tk

def openinfo(info_txt_path, x_cordinate, y_cordinate):
    infowin = tk.Tk()
    infowin.title('Inventory Salvage - Info')
    infowin.geometry("{}x{}+{}+{}".format(320, 240, x_cordinate, y_cordinate))
    infowin.resizable(False, False)
    text = ''
    with open(info_txt_path, 'r') as f:
        text = f.read()
    canvas = tk.Canvas(infowin)
    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar = tk.Scrollbar(infowin, orient="vertical", command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    canvas.configure(yscrollcommand=scrollbar.set)
    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")
    infotext = tk.Label(frame, text=text, anchor='nw', wraplength=300, justify='left')
    infotext.pack()
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    infowin.grid_rowconfigure(0, weight=1)
    infowin.grid_columnconfigure(0, weight=1)
    infowin.mainloop()
# modules/style_config.py
from tkinter import ttk, font

def setup_style():
    style = ttk.Style()
    style.theme_use('clam')  # 'clam' theme has a modern look, you can try 'vista' or 'alt'

    # Fonts
    main_font = ('Helvetica', 12)
    bold_font = font.nametofont('TkDefaultFont')
    bold_font.configure(weight='bold', size=12)

    # Button style
    style.configure('TButton', font=bold_font, borderwidth=2, relief='raised', background='#4CAF50', foreground='white')
    style.map('TButton', foreground=[('pressed', 'white'), ('active', 'black')],
              background=[('pressed', '!disabled', '#3e8e41'), ('active', '#66bb6a')])

    # Label style
    style.configure('TLabel', font=main_font, background='lightgray', foreground='black')

    # Entry and Combobox style
    style.configure('TEntry', foreground='black', fieldbackground='white', font=main_font)
    style.configure('TCombobox', fieldbackground='white', selectbackground='white', selectforeground='black', font=main_font)

    # Treeview style
    style.configure('Treeview', font=main_font, background='white', foreground='black', fieldbackground='lightgrey')
    style.map('Treeview', background=[('selected', 'lightblue')])
    
    # General Backgrounds
    style.configure('.', background='#f0f0f0')

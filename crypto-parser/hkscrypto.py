import requests
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.dates import DateFormatter
import webbrowser
from datetime import datetime, timedelta
import numpy as np
import threading
from PIL import Image, ImageTk
from io import BytesIO
import time
class CryptoParser:
    def __init__(self, root):
        self.root = root
        self.root.title("Crypto Parser")
        self.root.geometry("1400x900")
        self.root.configure(bg='#0f1923')
        self.setup_styles()
        self.create_widgets()
        self.coins = []
        self.selected_coin = None
        self.update_in_progress = False
        self.load_data()
        self.root.after(60000, self.update_data)
    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        bg_color = '#0f1923'
        card_color = '#1a2d3d'
        accent_color = '#1e3d59'
        text_color = 'white'
        self.style.configure('TFrame', background=bg_color)
        self.style.configure('TLabel', background=bg_color, foreground=text_color)
        self.style.configure('Treeview',
                             background=card_color,
                             fieldbackground=card_color,
                             foreground=text_color,
                             rowheight=30,
                             font=('Helvetica', 10))
        self.style.configure('Treeview.Heading',
                             background=accent_color,
                             foreground=text_color,
                             font=('Helvetica', 10, 'bold'))
        self.style.map('Treeview', background=[('selected', '#2a4d6e')])
        self.style.configure('TButton',
                             background=accent_color,
                             foreground=text_color,
                             font=('Helvetica', 10),
                             padding=5)
        self.style.map('TButton',
                       background=[('active', '#2a4d6e')])
        self.style.configure('TRadiobutton',
                             background=bg_color,
                             foreground=text_color,
                             font=('Helvetica', 9))
        self.style.configure('TEntry',
                             fieldbackground=card_color,
                             foreground=text_color,
                             insertcolor=text_color)
    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        bg_color = '#0f1923'
        card_color = '#1a2d3d'
        accent_color = '#1e3d59'
        text_color = 'white'
        self.style.configure('TFrame', background=bg_color)
        self.style.configure('TLabel', background=bg_color, foreground=text_color)
        self.style.configure('Treeview',
                             background=card_color,
                             fieldbackground=card_color,
                             foreground=text_color,
                             rowheight=30,
                             font=('Helvetica', 10))
        self.style.configure('Treeview.Heading',
                             background=accent_color,
                             foreground=text_color,
                             font=('Helvetica', 10, 'bold'))
        self.style.map('Treeview', background=[('selected', '#2a4d6e')])
        self.style.configure('TButton',
                             background=accent_color,
                             foreground=text_color,
                             font=('Helvetica', 10),
                             padding=5)
        self.style.map('TButton',
                       background=[('active', '#2a4d6e')])
        self.style.configure('TRadiobutton',
                             background=bg_color,
                             foreground=text_color,
                             font=('Helvetica', 9))
        self.style.configure('TEntry',
                             fieldbackground=card_color,
                             foreground=text_color,
                             insertcolor=text_color)
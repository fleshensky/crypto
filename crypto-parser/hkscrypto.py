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
    def create_widgets(self):
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill='x', padx=20, pady=(20, 10))

        self.logo_img = self.load_image_from_url(
            "https://cryptologos.cc/logos/versions/bitcoin-btc-logo-full.svg",
            size=(40, 40)
        )
        ttk.Label(header_frame, image=self.logo_img).pack(side='left')

        ttk.Label(
            header_frame,
            text="CRYPTO PARSER BINANCE",
            font=('Helvetica', 24, 'bold')
        ).pack(side='left', padx=5)
        search_frame = ttk.Frame(header_frame)
        search_frame.pack(side='right')
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=30,
            font=('Helvetica', 10)
        )
        search_entry.pack(side='left')
        search_entry.bind('<KeyRelease>', self.filter_coins)
        ttk.Button(
            search_frame,
            text="Search",
            command=self.filter_coins
        ).pack(side='left', padx=5)
        filter_frame = ttk.Frame(self.root)
        filter_frame.pack(fill='x', padx=20, pady=(0, 10))
        ttk.Label(filter_frame, text="Sort by:", font=('Helvetica', 10)).pack(side='left')
        self.sort_var = tk.StringVar(value='market_cap')
        sort_options = [
            ('Market Cap', 'market_cap'),
            ('Price ▲', 'price_asc'),
            ('Price ▼', 'price_desc'),
            ('24h % ▲', 'percent_asc'),
            ('24h % ▼', 'percent_desc'),
            ('Volume', 'volume'),
            ('A-Z', 'name_asc'),
            ('Z-A', 'name_desc')
        ]
        for text, mode in sort_options:
            ttk.Radiobutton(
                filter_frame,
                text=text,
                variable=self.sort_var,
                value=mode,
                command=self.sort_coins
            ).pack(side='left', padx=5)

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        list_frame = ttk.Frame(main_frame, width=450)
        list_frame.pack(side='left', fill='y')
        self.tree = ttk.Treeview(
            list_frame,
            columns=('name', 'price', 'change', 'volume'),
            show='headings',
            height=20
        )

        self.tree.heading('name', text='Coin', anchor='w')
        self.tree.heading('price', text='Price (USD)', anchor='center')
        self.tree.heading('change', text='24h %', anchor='center')
        self.tree.heading('volume', text='Volume (24h)', anchor='center')
        self.tree.column('name', width=180, anchor='w')
        self.tree.column('price', width=120, anchor='center')
        self.tree.column('change', width=80, anchor='center')
        self.tree.column('volume', width=120, anchor='center')
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        self.tree.bind('<<TreeviewSelect>>', self.show_coin_details)
        detail_frame = ttk.Frame(main_frame)
        detail_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        self.detail_header = ttk.Frame(detail_frame)
        self.detail_header.pack(fill='x', pady=(0, 10))
        self.price_frame = ttk.Frame(detail_frame)
        self.price_frame.pack(fill='x', pady=(0, 10))
        timeframe_frame = ttk.Frame(detail_frame)
        timeframe_frame.pack(fill='x', pady=(0, 10))
        ttk.Label(timeframe_frame, text="Timeframe:").pack(side='left')
        self.timeframe_var = tk.StringVar(value='7d')
        timeframes = [
            ('1D', '1d'),
            ('7D', '7d'),
            ('1M', '30d'),
            ('3M', '90d'),
            ('1Y', '365d'),
            ('All', 'max')
        ]
        for text, mode in timeframes:
            ttk.Radiobutton(
                timeframe_frame,
                text=text,
                variable=self.timeframe_var,
                value=mode,
                command=self.update_chart
            ).pack(side='left', padx=5)

        self.chart_frame = ttk.Frame(detail_frame)
        self.chart_frame.pack(fill='both', expand=True)
        self.info_frame = ttk.Frame(detail_frame)
        self.info_frame.pack(fill='x', pady=(10, 0))
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            relief='sunken',
            anchor='w',
            font=('Helvetica', 9)
        )
import tkinter as tk
from tkinter import ttk

class DepthAnalysisApp:
    def __init__(self, parent, symbol):
        self.window = parent
        self.symbol = symbol

        # Başlık
        ttk.Label(self.window, text=f"{self.symbol} Derinlik Verisi", font=("Arial", 16)).pack(pady=10)

        # Ana konteyner
        self.container = ttk.Frame(self.window)
        self.container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.setup_tables()
        self.update_depth_data()

        ttk.Button(self.window, text="Verileri Güncelle", command=self.update_depth_data).pack(pady=5)

    def setup_tables(self):
        if hasattr(self, 'buy_frame'):
            self.buy_frame.destroy()
        if hasattr(self, 'sell_frame'):
            self.sell_frame.destroy()

        self.buy_frame = ttk.LabelFrame(self.container, text="Alış Emirleri")
        self.buy_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.buy_tree = ttk.Treeview(self.buy_frame, columns=('Fiyat', 'Lot', 'Toplam'), show='headings')
        for col in ('Fiyat', 'Lot', 'Toplam'):
            self.buy_tree.heading(col, text=col)
            self.buy_tree.column(col, anchor='center')
        self.buy_tree.pack(fill=tk.BOTH, expand=True)

        self.sell_frame = ttk.LabelFrame(self.container, text="Satış Emirleri")
        self.sell_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.sell_tree = ttk.Treeview(self.sell_frame, columns=('Fiyat', 'Lot', 'Toplam'), show='headings')
        for col in ('Fiyat', 'Lot', 'Toplam'):
            self.sell_tree.heading(col, text=col)
            self.sell_tree.column(col, anchor='center')
        self.sell_tree.pack(fill=tk.BOTH, expand=True)

    def update_depth_data(self):
        # Mevcut verileri temizle
        for item in self.buy_tree.get_children():
            self.buy_tree.delete(item)
        for item in self.sell_tree.get_children():
            self.sell_tree.delete(item)

        # Örnek veriler (burayı Asenax API ile değiştirebilirsin)
        buy_orders = [
            (319.75, '1,715,105', '548,404,823.75'),
            (319.43, '857,552', '273,928,049.75'),
            (319.11, '571,701', '182,435,791.96'),
            (318.79, '428,776', '136,698,226.62'),
            (318.47, '343,021', '109,242,240.89')
        ]

        sell_orders = [
            (319.75, '1,715,105', '548,404,823.75'),
            (320.07, '857,552', '274,476,454.25'),
            (320.39, '571,701', '183,166,997.54'),
            (320.71, '428,776', '137,512,429.38'),
            (321.03, '343,021', '110,119,688.61')
        ]

        for order in buy_orders:
            self.buy_tree.insert('', 'end', values=order)

        for order in sell_orders:
            self.sell_tree.insert('', 'end', values=order)

import tkinter as tk
from tkinter import ttk

def on_menu_select(menu_item):
    print(f'{menu_item} selecionado')

root = tk.Tk()
root.title("Menu SPED")

# Configurar estilo moderno
style = ttk.Style(root)
style.theme_use('clam')

# Configurar menu principal
menu_bar = tk.Menu(root)

# Menu SPED Contribuições
sped_contribuicoes_menu = tk.Menu(menu_bar, tearoff=0)
sped_contribuicoes_menu.add_command(label="0150", command=lambda: on_menu_select("Sped Contribuições - 0150"))
sped_contribuicoes_menu.add_command(label="0500", command=lambda: on_menu_select("Sped Contribuições - 0500"))
menu_bar.add_cascade(label="Sped Contribuições", menu=sped_contribuicoes_menu)

# Menu SPED Fiscal
sped_fiscal_menu = tk.Menu(menu_bar, tearoff=0)
sped_fiscal_menu.add_command(label="0150", command=lambda: on_menu_select("Sped Fiscal - 0150"))
sped_fiscal_menu.add_command(label="0500", command=lambda: on_menu_select("Sped Fiscal - 0500"))
menu_bar.add_cascade(label="Sped Fiscal", menu=sped_fiscal_menu)

# Adicionar barra de menu à janela principal
root.config(menu=menu_bar)

root.mainloop()

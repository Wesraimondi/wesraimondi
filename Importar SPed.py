# WESLEY ROCHA RAIMUNDO - 15.10.2024


import tkinter as tk
from tkinter import filedialog
import pandas as pd
import os

# Função para importar SPED e converter para Excel
def importar_sped_para_excel():
    caminho_sped = filedialog.askopenfilename(title="Selecione o arquivo SPED")
    if caminho_sped:
        nome_arquivo, _ = os.path.splitext(os.path.basename(caminho_sped))
        caminho_excel = os.path.join(os.path.dirname(caminho_sped), f'{nome_arquivo}.xlsx')
        
        linhas = []
        with open(caminho_sped, 'r') as arquivo:
            for linha in arquivo:
                partes = linha.strip().split('|')
                linhas.append(partes)
        df = pd.DataFrame(linhas)
        df.to_excel(caminho_excel, index=False, header=False)
        print(f'Arquivo Excel gerado: {caminho_excel}')

# Função para importar Excel e converter para SPED
def importar_excel_para_sped():
    caminho_excel = filedialog.askopenfilename(title="Selecione o arquivo Excel")
    if caminho_excel:
        nome_arquivo, _ = os.path.splitext(os.path.basename(caminho_excel))
        caminho_sped = os.path.join(os.path.dirname(caminho_excel), f'{nome_arquivo}.txt')
        
        df = pd.read_excel(caminho_excel, header=None)
        with open(caminho_sped, 'w') as arquivo:
            for _, row in df.iterrows():
                linha = '|'.join(row.astype(str))
                arquivo.write(linha + '\n')
        print(f'Arquivo SPED gerado: {caminho_sped}')

# Configuração da interface Tkinter
root = tk.Tk()
root.title("Conversor SPED <=> Excel")

frame = tk.Frame(root)
frame.pack(pady=20)

importar_button = tk.Button(frame, text="Importar SPED e Converter para Excel", command=importar_sped_para_excel)
importar_button.pack(pady=10)

exportar_button = tk.Button(frame, text="Importar Excel e Converter para SPED", command=importar_excel_para_sped)
exportar_button.pack(pady=10)

root.mainloop()

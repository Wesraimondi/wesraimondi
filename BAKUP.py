import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from zipfile import ZipFile
from datetime import datetime

# Função para buscar arquivos de Excel e Word
def buscar_arquivos(diretorio):
    extensoes = ['.xlsx', '.xls', '.xlsm', '.doc', '.docx']
    arquivos_encontrados = []

    for raiz, _, arquivos in os.walk(diretorio):
        for arquivo in arquivos:
            if any(arquivo.endswith(ext) for ext in extensoes):
                arquivos_encontrados.append(os.path.join(raiz, arquivo))

    return arquivos_encontrados

# Função para criar backup e compactar os arquivos
def criar_backup(diretorio_destino):
    arquivos_encontrados = buscar_arquivos("C:/Users/Wesley.Raimundo/Desktop")  # Percorre todo o PC a partir do C:/
    
    if not arquivos_encontrados:
        messagebox.showinfo("Informação", "Nenhum arquivo do Excel ou Word encontrado.")
        return
    
    # Nome do arquivo ZIP com data e hora
    data_hora = datetime.now().strftime("%d_%m_%Y_%H%M%S")
    caminho_zip = os.path.join(diretorio_destino, f"backup_{data_hora}.zip")

    total_arquivos = len(arquivos_encontrados)

    # Cria um arquivo ZIP e adiciona os arquivos encontrados
    with ZipFile(caminho_zip, 'w') as zipf:
        for i, arquivo in enumerate(arquivos_encontrados):
            try:
                # Adiciona o arquivo ao ZIP
                zipf.write(arquivo, os.path.relpath(arquivo, start=os.path.dirname(arquivo)))
                
                # Atualiza a barra de progresso
                progresso.set((i + 1) / total_arquivos * 100)
                janela.update_idletasks()
            except Exception as e:
                print(f"Erro ao adicionar {arquivo} ao ZIP: {e}")

    messagebox.showinfo("Conclusão", f"Backup concluído! Arquivo salvo em: {caminho_zip}")

# Função para abrir o diálogo de seleção de pasta
def selecionar_destino():
    pasta_destino = filedialog.askdirectory()
    if pasta_destino:
        criar_backup(pasta_destino)

# Criando a interface gráfica
janela = tk.Tk()
janela.title("Sistema de Backup")
janela.geometry("400x200")

# Barra de progresso
progresso = tk.DoubleVar()
barra_progresso = ttk.Progressbar(janela, variable=progresso, maximum=100)
barra_progresso.pack(pady=20, fill=tk.X, padx=20)

# Botão para iniciar o backup
botao_backup = tk.Button(janela, text="Selecionar Destino e Iniciar Backup", command=selecionar_destino)
botao_backup.pack(pady=10)

janela.mainloop()

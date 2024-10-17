import tkinter as tk
from tkinter import filedialog

def atualizar_registros_sped(arquivo_entrada):
    novo_valor = "4.1.01.03.0013"
    
    with open(arquivo_entrada, 'r', encoding='utf-8') as file:
        linhas = file.readlines()
    
    linhas_atualizadas = []
    
    for linha in linhas:
        if linha.startswith('|C501|') or linha.startswith('|C505|'):
            campos = linha.strip().split('|')  # Supondo que os campos sejam separados por '|'
            if len(campos) > 8:  # Verifica se há pelo menos 8 campos
                campos[8] = "4.1.01.03.0013" # Atualiza o campo 8
            linha = '|'.join(campos) + '\n'
        
        linhas_atualizadas.append(linha)
    
    # Salva as linhas atualizadas no mesmo arquivo
    with open(arquivo_entrada, 'w', encoding='utf-8') as file:
        file.writelines(linhas_atualizadas)

def selecionar_arquivo():
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal

    # Seleciona o arquivo a ser editado
    arquivo_entrada = filedialog.askopenfilename(title="Selecione o arquivo SPED para editar", filetypes=[("Text files", "*.txt")])
    if not arquivo_entrada:  # Verifica se um arquivo foi selecionado
        print("Nenhum arquivo selecionado.")
        return
    
    # Atualiza os registros
    atualizar_registros_sped(arquivo_entrada)
    print(f"Arquivo atualizado: {arquivo_entrada}")

# Chama a função para selecionar o arquivo
selecionar_arquivo()

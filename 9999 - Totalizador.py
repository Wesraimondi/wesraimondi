import tkinter as tk
from tkinter import filedialog

# Função para selecionar o arquivo
def selecionar_arquivo():
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal do Tkinter
    arquivo = filedialog.askopenfilename(title="Selecione o arquivo SPED", filetypes=[("Arquivos de texto", "*.txt")])
    return arquivo

# Função para ler e contar registros
def contar_registros(arquivo):
    registros = {}
    
    with open(arquivo, 'r', encoding='utf-8') as f:
        for linha in f:
            # Divide a linha no caractere separador "|"
            campos = linha.split('|')
            
            if len(campos) > 1:
                registro = campos[1]
                
                # Contabiliza os registros
                if registro in registros:
                    registros[registro] += 1
                else:
                    registros[registro] = 1
    
    return registros

# Função para calcular os totalizadores finais
def calcular_totalizadores(registros):
    total_9900 = len(registros) + 3  # +3 para incluir o 9900, 9990 e 9999
    total_9990 = total_9900 + 1  # O registro 9990 inclui o total do 9900
    total_9999 = sum(registros.values()) + total_9990  # Soma todos os registros contados + 9990
    
    registros['9900'] = total_9900  # Total de linhas de registro no 9900
    registros['9990'] = total_9990  # Total de linhas de registro no 9990
    registros['9999'] = total_9999  # Total geral de linhas no arquivo
    
    return registros

# Função para inserir ou atualizar o registro 9900, 9990 e 9999
def inserir_ou_atualizar_registros(arquivo, registros):
    novo_arquivo = arquivo.replace('.txt', '_totalizado.txt')
    
    with open(arquivo, 'r', encoding='utf-8') as f:
        linhas = f.readlines()

    registros_existentes = {}
    
    # Processa as linhas do arquivo e verifica se já existem totalizadores 9900, 9990, 9999
    for i, linha in enumerate(linhas):
        campos = linha.split('|')
        if len(campos) > 1 and campos[1] == '9900':
            registro = campos[2]
            total = int(campos[3])
            registros_existentes[registro] = (i, total)

    with open(novo_arquivo, 'w', encoding='utf-8') as f:
        for i, linha in enumerate(linhas):
            # Atualiza os registros 9900 existentes
            campos = linha.split('|')
            if len(campos) > 1 and campos[1] == '9900':
                registro = campos[2]
                if registro in registros:
                    total_atualizado = registros[registro]
                    f.write(f'|9900|{registro}|{total_atualizado}|\n')
                    registros.pop(registro)
                else:
                    f.write(linha)
            else:
                f.write(linha)
            
            # Quando encontrar o registro 9001, insere os totalizadores 9900, 9990, 9999
            if '|9001|' in linha:
                for reg, total in registros.items():
                    f.write(f'|9900|{reg}|{total}|\n')
                f.write(f'|9990|{registros["9990"]}|\n')
                f.write(f'|9999|{registros["9999"]}|\n')

    print(f"Arquivo totalizado salvo como: {novo_arquivo}")

# Função principal
def main():
    arquivo = selecionar_arquivo()
    if arquivo:
        registros = contar_registros(arquivo)
        registros = calcular_totalizadores(registros)
        inserir_ou_atualizar_registros(arquivo, registros)
    else:
        print("Nenhum arquivo selecionado.")

if __name__ == "__main__":
    main()

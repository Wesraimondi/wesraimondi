import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
import logging

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Credenciais de exemplo (em um sistema real, isso seria armazenado de forma segura)
USUARIO_CORRETO = "wesley"
SENHA_CORRETA = "210769"

def verificar_login(janela, usuario, senha):
    if usuario.get() == USUARIO_CORRETO and senha.get() == SENHA_CORRETA:
        janela.destroy()
        executar_programa_principal()
    else:
        messagebox.showerror("Erro de Login", "Usuário ou senha incorretos")
        logger.warning(f"Tentativa de login falhou para o usuário: {usuario.get()}")

def tela_login():
    janela = tk.Tk()
    janela.title("Login")
    janela.geometry("300x150")

    tk.Label(janela, text="Usuário:").pack()
    usuario = tk.Entry(janela)
    usuario.pack()

    tk.Label(janela, text="Senha:").pack()
    senha = tk.Entry(janela, show="*")
    senha.pack()

    tk.Button(janela, text="Login", command=lambda: verificar_login(janela, usuario, senha)).pack()

    janela.mainloop()

def selecionar_arquivo():
    root = tk.Tk()
    root.withdraw()
    caminho_arquivo = filedialog.askopenfilename(title="Selecione o arquivo SPED", filetypes=[("Text files", "*.txt")])
    return caminho_arquivo

def ler_arquivo_sped(caminho_arquivo):
    with open(caminho_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
    logger.info(f"Arquivo lido: {caminho_arquivo}")
    return linhas

def editar_registros(linhas):
    linhas_alteradas = []
    campos_c197 = ['1302', '1407', '1551', '1556', '1901', '1902', '1908', '1910', '1915', '1916', '1920', '1921', '1949', '2302', '2551', '2902', '2915', '3556', '5101', '5901', '5902', '5903', '5909', '5915', '5916', '5920', '5949', '6916', '6923', '7101', '7102', '7949', '6101', '6102', '6949']
    for i, linha in enumerate(linhas):
        partes = linha.strip().split('|')
        if partes[1] == "0150":
            if partes[8][:2] == "31" and len(partes[7]) < 13:  # CORRIGE O TAMANHO DO CNPJ DO ESTADO DE MG
                partes[7] = "0" * (13 - len(partes[7])) + partes[7]
                nova_linha = '|'.join(partes)
                linhas[i] = nova_linha + '\n'
                linhas_alteradas.append(nova_linha)
            if partes[4] != '1058':
                partes[5] = ''  # Apaga a informação no campo 5 (CNPJ - QUANDO NÃO FOR EMPRESA DO BRASIL)
                nova_linha = '|'.join(partes)
                linhas[i] = nova_linha + '\n'
                linhas_alteradas.append(nova_linha)
            if len(partes[8]) < 7:
                partes[7] = ''  # Deixa o campo 7 vazio (REGISTRO CÓDIGO DO MUNICIPIO)
                nova_linha = '|'.join(partes)
                linhas[i] = nova_linha + '\n'
                linhas_alteradas.append(nova_linha)

        elif partes[1] == "C170":
            primeiro_digito = partes[3][0]
            if primeiro_digito == '1':
                partes[37] = '1.1.10.01.0001'
            elif primeiro_digito == '2':
                partes[37] = '1.1.10.01.0002'
            elif primeiro_digito == '3':
                partes[37] = '1.1.10.01.0003'
            elif primeiro_digito == '4':
                partes[37] = '1.1.10.01.0004'
            elif primeiro_digito == '5':
                partes[37] = '1.1.10.01.0005'
            elif primeiro_digito in ['6', '7']:
                partes[37] = '1.1.10.01.0006'
            elif primeiro_digito == 'R':
                partes[37] = '3.1.01.01.0004'
            elif primeiro_digito == '0':
                partes[37] = '2.1.02.04.0099'
            nova_linha = '|'.join(partes)
            linhas[i] = nova_linha + '\n'
            linhas_alteradas.append(nova_linha)
        elif partes[1] == "C197":
            if partes[3] in campos_c197 and partes[7].strip() and float(partes[7]) > 0:
                partes[8] = partes[7]
                partes[7] = ''
                nova_linha = '|'.join(partes)
                linhas[i] = nova_linha + '\n'
                linhas_alteradas.append(nova_linha)
    logger.info(f"Total de linhas alteradas: {len(linhas_alteradas)}")
    return linhas, linhas_alteradas

def escrever_arquivo_sped(caminho_arquivo, linhas):
    agora = datetime.now()
    timestamp = agora.strftime("%Y")
    novo_nome_arquivo = f"{caminho_arquivo[:-4]}_{timestamp}.txt"
    
    with open(novo_nome_arquivo, 'w') as arquivo:
        arquivo.writelines(linhas)
    logger.info(f"Arquivo salvo como: {novo_nome_arquivo}")

def verificar_e_adicionar_registro(novo_registro, registros_existentes):
    campo6_novo = novo_registro.split('|')[6]
    for registro in registros_existentes:
        partes = registro.split('|')
    
        if len(partes) > 6:
            campo6_existente = partes[6]
            if campo6_novo == campo6_existente:
                logger.info(f"Registro com campo 6 '{campo6_novo}' já existe. Ignorando.")
                return registros_existentes
    
    posicao_insercao = len(registros_existentes)
    for i, registro in enumerate(registros_existentes):
        if registro.split('|')[1] == "0990":
            posicao_insercao = i
            break
        elif registro.split('|')[1] == "0500":
            posicao_insercao = i + 1

    registros_existentes.insert(posicao_insercao, novo_registro + '\n')
    logger.info(f"Registro com campo 6 '{campo6_novo}' adicionado na posição {posicao_insercao}.")
    return registros_existentes

def atualizar_registro_0990(linhas):
    total_registros = sum(1 for linha in linhas if linha.startswith('|0'))
    for i, linha in enumerate(linhas):
        if linha.startswith('|0990|'):
            partes = linha.strip().split('|')
            partes[2] = str(total_registros)
            linhas[i] = '|'.join(partes) + '\n'
            logger.info(f"Registro 0990 atualizado com o total de {total_registros} registros.")
            return linhas

    linhas.append(f"|0990|{total_registros}|\n")
    logger.info(f"Registro 0990 adicionado com o total de {total_registros} registros.")
    return linhas
        
def atualizar_registro_0500_9900(linhas):
    total_registros = sum(1 for linha in linhas if linha.startswith('|0500|'))
    for i, linha in enumerate(linhas):
        if linha.startswith('|9900|0500|'):
            partes = linha.strip().split('|')
            partes[3] = str(total_registros)
            linhas[i] = '|'.join(partes) + '\n'
            logger.info(f"Registro 0500 atualizado com o total de {total_registros} registros.")
            return linhas

    linhas.append(f"|9900|0500| {total_registros}|\n")
    logger.info(f"Registro 0990 adicionado com o total de {total_registros} registros.")
    return linhas

def atualizar_registro_9900(linhas):
    total_registros = sum(1 for linha in linhas if linha.startswith('|'))
    for i, linha in enumerate(linhas):
        if linha.startswith('|9999'):
            partes = linha.strip().split("|")
            partes[2] = str(total_registros)
            linhas[i] = '|'.join(partes) + '\n'
            logger.info(f"Registro 9999 atualizado com o total de {total_registros} registros.")
            return linhas

    linhas.append(f"|9999|{total_registros}|\n")
    logger.info(f"Registro 9999 adicionado com o total de {total_registros} registros.")
    return linhas

def verificar_e_adicionar_multiplos_registros(novos_registros, registros_existentes):
    for novo_registro in novos_registros:
        campo6_novo = novo_registro.split('|')[6]
        for registro in registros_existentes:
            partes = registro.split('|')
        
            if len(partes) > 6:
                campo6_existente = partes[6]
                if campo6_novo == campo6_existente:
                    logger.info(f"Registro com campo 6 '{campo6_novo}' já existe. Ignorando.")
                    break
        else:
            posicao_insercao = len(registros_existentes)
            for i, registro in enumerate(registros_existentes):
                if registro.split('|')[1] == "0990":
                    posicao_insercao = i
                    break
                elif registro.split('|')[1] == "0500":
                    posicao_insercao = i + 1
            
            registros_existentes.insert(posicao_insercao, novo_registro + '\n')
            logger.info(f"Registro com campo 6 '{campo6_novo}' adicionado na posição {posicao_insercao}.")
    return registros_existentes

def executar_programa_principal():
    novos_registros = [
        "|0500|01012009|01|A|5|1.1.10.01.0003|Material de Embalagem|1.01.03.02.02|62522453000135|",
        "|0500|01012009|01|A|5|1.1.10.01.0001|Matéria Prima|1.01.03.02.01|62522453000135|",
        # ... (outros registros)
    ]

    caminho_arquivo = selecionar_arquivo()

    if caminho_arquivo:
        linhas = ler_arquivo_sped(caminho_arquivo)
        linhas_editadas, linhas_alteradas = editar_registros(linhas)
        linhas_editadas = verificar_e_adicionar_multiplos_registros(novos_registros, linhas_editadas)
        linhas_editadas = atualizar_registro_0990(linhas_editadas)
        linhas_editadas = atualizar_registro_9900(linhas_editadas)
        linhas_editadas = atualizar_registro_0500_9900(linhas_editadas)
        escrever_arquivo_sped(caminho_arquivo, linhas_editadas)

        logger.info("Linhas alteradas:")
        for linha in linhas_alteradas:
            logger.info(linha)

        logger.info("Arquivo editado com sucesso!")
    else:
        logger.warning("Nenhum arquivo foi selecionado.")

if __name__ == "__main__":
    tela_login()

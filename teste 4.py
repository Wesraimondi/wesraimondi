import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime
import logging
import os
import csv
from typing import List, Tuple

# Configuração do logging
def setup_logging():
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file = os.path.join(log_dir, f"sped_processing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler(log_file),
                            logging.StreamHandler()
                        ])
    return logging.getLogger(__name__)

logger = setup_logging()

# Credenciais de exemplo (em um sistema real, isso seria armazenado de forma segura)
USUARIO_CORRETO = "wesley"
SENHA_CORRETA = "210769"

def verificar_login(janela: tk.Tk, usuario: tk.Entry, senha: tk.Entry):
    if usuario.get() == USUARIO_CORRETO and senha.get() == SENHA_CORRETA:
        logger.info(f"Login bem-sucedido para o usuário: {usuario.get()}")
        janela.destroy()
        mostrar_interface_principal()
    else:
        messagebox.showerror("Erro de Login", "Usuário ou senha incorretos")
        logger.warning(f"Tentativa de login falhou para o usuário: {usuario.get()}")

def tela_login():
    janela = tk.Tk()
    janela.title("Login - Processador SPED")
    janela.geometry("300x150")

    tk.Label(janela, text="Usuário:").pack()
    usuario = tk.Entry(janela)
    usuario.pack()

    tk.Label(janela, text="Senha:").pack()
    senha = tk.Entry(janela, show="*")
    senha.pack()

    tk.Button(janela, text="Login", command=lambda: verificar_login(janela, usuario, senha)).pack()

    janela.mainloop()

def mostrar_interface_principal():
    janela = tk.Tk()
    janela.title("Processador SPED")
    janela.geometry("400x300")

    tk.Button(janela, text="Processar Arquivo Único", command=processar_arquivo_unico).pack(pady=10)
    tk.Button(janela, text="Processar Múltiplos Arquivos", command=processar_multiplos_arquivos).pack(pady=10)
    tk.Button(janela, text="Gerar Relatório de Alterações", command=gerar_relatorio_alteracoes).pack(pady=10)
    tk.Button(janela, text="Sair", command=janela.quit).pack(pady=10)

    janela.mainloop()

def selecionar_arquivo() -> str:
    root = tk.Tk()
    root.withdraw()
    caminho_arquivo = filedialog.askopenfilename(title="Selecione o arquivo SPED", filetypes=[("Text files", "*.txt")])
    return caminho_arquivo

def selecionar_multiplos_arquivos() -> List[str]:
    root = tk.Tk()
    root.withdraw()
    caminhos_arquivos = filedialog.askopenfilenames(title="Selecione os arquivos SPED", filetypes=[("Text files", "*.txt")])
    return list(caminhos_arquivos)

def ler_arquivo_sped(caminho_arquivo: str) -> List[str]:
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()
        logger.info(f"Arquivo lido: {caminho_arquivo}")
        return linhas
    except Exception as e:
        logger.error(f"Erro ao ler o arquivo {caminho_arquivo}: {str(e)}")
        return []

def editar_registros(linhas: List[str]) -> Tuple[List[str], List[str]]:
    linhas_alteradas = []
    campos_c197 = ['1302', '1407', '1551', '1556', '1901', '1902', '1908', '1910', '1915', '1916', '1920', '1921', '1949', '2302', '2551', '2902', '2915', '3556', '5101', '5901', '5902', '5903', '5909', '5915', '5916', '5920', '5949', '6916', '6923', '7101', '7102', '7949', '6101', '6102', '6949']
    
    for i, linha in enumerate(linhas):
        partes = linha.strip().split('|')
        if partes[1] == "0150":
            if partes[8][:2] == "31" and len(partes[7]) < 13:
                partes[7] = "0" * (13 - len(partes[7])) + partes[7]
                nova_linha = '|'.join(partes)
                linhas[i] = nova_linha + '\n'
                linhas_alteradas.append(nova_linha)
            if partes[4] != '1058':
                partes[5] = ''
                nova_linha = '|'.join(partes)
                linhas[i] = nova_linha + '\n'
                linhas_alteradas.append(nova_linha)
            if len(partes[8]) < 7:
                partes[7] = ''
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

def escrever_arquivo_sped(caminho_arquivo: str, linhas: List[str]) -> str:
    agora = datetime.now()
    timestamp = agora.strftime("%Y%m%d_%H%M%S")
    novo_nome_arquivo = f"{os.path.splitext(caminho_arquivo)[0]}_{timestamp}.txt"
    
    try:
        with open(novo_nome_arquivo, 'w', encoding='utf-8') as arquivo:
            arquivo.writelines(linhas)
        logger.info(f"Arquivo salvo como: {novo_nome_arquivo}")
        return novo_nome_arquivo
    except Exception as e:
        logger.error(f"Erro ao escrever o arquivo {novo_nome_arquivo}: {str(e)}")
        return ""

# Função para verificar e adicionar registros
def verificar_e_adicionar_registro(novo_registro, registros_existentes):
    campo6_novo = novo_registro.split('|')[6]
    for registro in registros_existentes:
        partes = registro.split('|')
    
        if len(partes) > 6:
            campo6_existente = partes[6]
            if campo6_novo == campo6_existente:
                print(f"Registro com campo 6 '{campo6_novo}' já existe. Ignorando.")
                return registros_existentes

def atualizar_registro_0990(linhas: List[str]) -> List[str]:
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

def atualizar_registro_0500_9900(linhas: List[str]) -> List[str]:
    total_registros = sum(1 for linha in linhas if linha.startswith('|0500|'))
    for i, linha in enumerate(linhas):
        if linha.startswith('|9900|0500|'):
            partes = linha.strip().split('|')
            partes[3] = str(total_registros)
            linhas[i] = '|'.join(partes) + '\n'
            logger.info(f"Registro 0500 atualizado com o total de {total_registros} registros.")
            return linhas

    linhas.append(f"|9900|0500|{total_registros}|\n")
    logger.info(f"Registro 9900|0500 adicionado com o total de {total_registros} registros.")
    return linhas

def atualizar_registro_9900(linhas: List[str]) -> List[str]:
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

def processar_arquivo(caminho_arquivo: str) -> Tuple[str, List[str]]:
    linhas = ler_arquivo_sped(caminho_arquivo)
    if not linhas:
        return "", []

    linhas_editadas, linhas_alteradas = editar_registros(linhas)
    linhas_editadas = atualizar_registro_0990(linhas_editadas)
    linhas_editadas = atualizar_registro_9900(linhas_editadas)
    linhas_editadas = atualizar_registro_0500_9900(linhas_editadas)
    
    novo_arquivo = escrever_arquivo_sped(caminho_arquivo, linhas_editadas)
    return novo_arquivo, linhas_alteradas
# Novo registro com mais informações
    novo_registro = "|0500|01012009|01|A|5|1.1.10.01.0003|Material de Embalagem|1.01.03.02.02|62522453000135|"
    novo_registro2 = "|0500|01012009|01|A|5|1.1.10.01.0001|Matéria Prima|1.01.03.02.01|62522453000135|"
    novo_registro3 = "|0500|01012009|01|A|5|1.1.10.01.0002|Material Secundário|1.01.03.02.01|62522453000135|"
    novo_registro4 = "|0500|01012009|01|A|5|1.1.10.01.0001|Matéria Prima|1.01.03.02.01|62522453000135|"
    novo_registro5 = "|0500|01012009|01|A|5|1.1.10.01.0002|Material Secundário|1.01.03.02.01|62522453000135|"
    novo_registro6 = "|0500|01012009|01|A|5|1.1.10.01.0003|Material de Embalagem|1.01.03.02.02|62522453000135|"
    novo_registro7 = "|0500|01012009|01|A|5|1.1.10.01.0005|Produtos Acabados|1.01.03.02.04|62522453000135|"
    novo_registro8 = "|0500|01012009|01|A|5|1.1.10.01.0006|Mercadorias Para Revenda|1.01.03.01.01|62522453000135|"
    novo_registro9 = "|0500|01012009|02|A|5|2.1.02.04.0099|Trânsito Valores à Classificar|2.01.01.17.28|62522453000135|"
    novo_registro10 = "|0500|01012008|02|A|5|2.1.02.01.0002|Fornecedores de Outros Serviços|2.01.01.03.01|62522453000135|"
    novo_registro11 = "|0500|01012008|04|A|5|3.1.01.01.0005|Serviços Executados|3.01.01.01.01.06|62522453000135|"
    novo_registro12 = "|0500|01012009|04|A|5|3.1.01.01.0001|Vendas Para o Estado|3.01.01.01.01.04|62522453000135|"
    novo_registro13 = "|0500|01012008|04|A|5|4.1.01.03.0013|Energia Eletrica|3.01.01.03.01.01|62522453000135|"
    novo_registro14 = "|0500|01012009|04|A|5|3.1.01.01.0002|Vendas Para Outros Estados|3.01.01.01.01.04|62522453000135|"
    novo_registro15 = "|0500|01012009|04|A|5|3.1.01.01.0003|Vendas Para o Exterior|3.01.01.01.01.01|62522453000135|"
    novo_registro16 = "|0500|01012009|04|A|5|3.1.01.01.0004|Revenda de Produtos|3.01.01.01.01.05|62522453000135|"
    novo_registro17 = "|0500|01012009|04|A|5|4.1.01.03.0016|Manut.Predios e Instalaçoes|3.01.01.03.01.01|62522453000135|"
    novo_registro18 = "|0500|01012009|04|A|5|4.1.01.03.0032|xxxxxxxxxxxxxx|3.01.01.03.01.01|62522453000135|"
    novo_registro19 = "|0500|01012009|04|A|5|4.1.01.03.0041|xxxxxxxxxxxxxx|3.01.01.03.01.01|62522453000135|"
    novo_registro20 = "|0500|01012009|04|A|5|4.1.01.03.0006|xxxxxxxxxxxxxx|3.01.01.03.01.01|62522453000135|"
    novo_registro21 = "|0500|01012009|04|A|5|4.1.01.02.0014|xxxxxxxxxxxxxx|3.01.01.03.01.01|62522453000135|"

# Lista de novos registros
novos_registros = [
    novo_registro,
    novo_registro2,
    novo_registro3,
    novo_registro4,
    novo_registro5,
    novo_registro6,
    novo_registro7,
    novo_registro8,
    novo_registro9,
    novo_registro10,
    novo_registro11,
    novo_registro12,
    novo_registro13,
    novo_registro14,
    novo_registro15,
    novo_registro16,
    novo_registro17,
    novo_registro18,
    novo_registro19,
    novo_registro20,
    novo_registro21,
]

def processar_arquivo_unico():
    caminho_arquivo = selecionar_arquivo()
    if caminho_arquivo:
        novo_arquivo, linhas_alteradas = processar_arquivo(caminho_arquivo)
        if novo_arquivo:
            messagebox.showinfo("Sucesso", f"Arquivo processado e salvo como:\n{novo_arquivo}")
            logger.info(f"Arquivo processado com sucesso: {novo_arquivo}")
        else:
            messagebox.showerror("Erro", "Falha ao processar o arquivo.")
            logger.error("Falha ao processar o arquivo.")
    else:
        logger.warning("Nenhum arquivo foi selecionado.")

def processar_multiplos_arquivos():
    caminhos_arquivos = selecionar_multiplos_arquivos()
    if caminhos_arquivos:
        resultados = []
        for caminho in caminhos_arquivos:
            novo_arquivo, _ = processar_arquivo(caminho)
            if novo_arquivo:
                resultados.append(f"Processado: {caminho} -> {novo_arquivo}")
            else:
                resultados.append(f"Falha: {caminho}")
        
        messagebox.showinfo("Resultado", "\n".join(resultados))
        logger.info(f"Processamento em lote concluído. Total de arquivos: {len(caminhos_arquivos)}")
    else:
        logger.warning("Nenhum arquivo foi selecionado para processamento em lote.")

def gerar_relatorio_alteracoes():
    caminho_arquivo = selecionar_arquivo()
    if caminho_arquivo:
        _, linhas_alteradas = processar_arquivo(caminho_arquivo)
        if linhas_alteradas:
            nome_relatorio = f"relatorio_alteracoes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(nome_relatorio, 'w', newline='', encoding='utf-8') as arquivo_csv:
                writer = csv.writer(arquivo_csv)
                writer.writerow(['Linha Alterada'])
                for linha in linhas_alteradas:
                    writer.writerow([linha])
            messagebox.showinfo("Sucesso", f"Relatório de alterações gerado:\n{nome_relatorio}")
            logger.info(f"Relatório de alterações gerado: {nome_relatorio}")
        else:
            messagebox.showinfo("Informação", "Nenhuma alteração foi feita no arquivo.")
            logger.info("Nenhuma alteração foi feita no arquivo para gerar o relatório.")
    else:
        logger.warning("Nenhum arquivo foi selecionado para gerar o relatório de alterações.")

if __name__ == "__main__":
    tela_login()

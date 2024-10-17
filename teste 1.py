import tkinter as tk
from tkinter import filedialog
from datetime import datetime

def selecionar_arquivo():
    root = tk.Tk()
    root.withdraw()
    caminho_arquivo = filedialog.askopenfilename(title="Selecione o arquivo SPED", filetypes=[("Text files", "*.txt")])
    return caminho_arquivo

def ler_arquivo_sped(caminho_arquivo):
    with open(caminho_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
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
    return linhas, linhas_alteradas

def escrever_arquivo_sped(caminho_arquivo, linhas):
    # Obter a data e hora atuais
    agora = datetime.now()
    timestamp = agora.strftime("%Y")
    # Criar o novo nome do arquivo
    novo_nome_arquivo = f"{caminho_arquivo[:-4]}_{timestamp}.txt"
    
    with open(novo_nome_arquivo, 'w') as arquivo:
        arquivo.writelines(linhas)
    print(f"Arquivo salvo como: {novo_nome_arquivo}")

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
    
    # Encontrar a posição correta para inserir o novo registro 0500
    posicao_insercao = len(registros_existentes)
    for i, registro in enumerate(registros_existentes):
        if registro.split('|')[1] == "0990":
            posicao_insercao = i
            break
        elif registro.split('|')[1] == "0500":
            posicao_insercao = i + 1

    
    registros_existentes.insert(posicao_insercao, novo_registro + '\n')
    print(f"Registro com campo 6 '{campo6_novo}' adicionado na posição {posicao_insercao}.")
    return registros_existentes

# Função para atualizar o registro 0990
def atualizar_registro_0990(linhas):
    total_registros = sum(1 for linha in linhas if linha.startswith('|0'))
    for i, linha in enumerate(linhas):
        if linha.startswith('|0990|'):
            partes = linha.strip().split('|')
            partes[2] = str(total_registros)
            linhas[i] = '|'.join(partes) + '\n'
            print(f"Registro 0990 atualizado com o total de {total_registros} registros.")
            return linhas

    # Se o registro 0990 não existir, adicionar no final
    linhas.append(f"|0990|{total_registros}|\n")
    print(f"Registro 0990 adicionado com o total de {total_registros} registros.")
    return linhas
        
# Função para atualizar o registro 9900|0500
def atualizar_registro_0500_9900(linhas):
    total_registros = sum(1 for linha in linhas if linha.startswith('|0500|'))
    for i, linha in enumerate(linhas):
        if linha.startswith('|9900|0500|'):
            partes = linha.strip().split('|')
            partes[3] = str(total_registros)
            linhas[i] = '|'.join(partes) + '\n'
            print(f"Registro 0500 atualizado com o total de {total_registros} registros.")
            return linhas

# Se o registro 0990 não existir, adicionar no final
    linhas.append(f"|9900|0500| {total_registros}|\n")
    print(f"Registro 0990 adicionado com o total de {total_registros} registros.")
    return linhas

# Função para atualizar o registro 9999
def atualizar_registro_9900(linhas):
    total_registros = sum(1 for linha in linhas if linha.startswith('|'))
    for i, linha in enumerate(linhas):
        if linha.startswith('|9999'):
            partes = linha.strip().split("|")
            partes[2] = str(total_registros)
            linhas[i] = '|'.join(partes) + '\n'
            print(f"Registro 9999 atualizado com o total de {total_registros} registros.")
            return linhas

# Se o registro 9999 não existir, adicionar no final
    linhas.append(f"|9999|{total_registros}|\n")
    print(f"Registro 9999 adicionado com o total de {total_registros} registros.")
    return linhas
        


# Seleção do arquivo
caminho_arquivo = selecionar_arquivo()

if caminho_arquivo:
    # Leitura do arquivo
    linhas = ler_arquivo_sped(caminho_arquivo)

    # Edição dos registros
    linhas_editadas, linhas_alteradas = editar_registros(linhas)

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




# Função para verificar e adicionar múltiplos registros
def verificar_e_adicionar_multiplos_registros(novos_registros, registros_existentes):
    for novo_registro in novos_registros:
        campo6_novo = novo_registro.split('|')[6]
        for registro in registros_existentes:
            partes = registro.split('|')
        
            if len(partes) > 6:
                campo6_existente = partes[6]
                if campo6_novo == campo6_existente:
                    print(f"Registro com campo 6 '{campo6_novo}' já existe. Ignorando.")
                    break
        else:
            # Encontrar a posição correta para inserir o novo registro 0500
            posicao_insercao = len(registros_existentes)
            for i, registro in enumerate(registros_existentes):
                if registro.split('|')[1] == "0990":
                    posicao_insercao = i
                    break
                elif registro.split('|')[1] == "0500":
                    posicao_insercao = i + 1
            
            registros_existentes.insert(posicao_insercao, novo_registro + '\n')
            print(f"Registro com campo 6 '{campo6_novo}' adicionado na posição {posicao_insercao}.")
    return registros_existentes

# Seleção do arquivo
caminho_arquivo = selecionar_arquivo()

if caminho_arquivo:
    # Leitura do arquivo
    linhas = ler_arquivo_sped(caminho_arquivo)

    # Edição dos registros
    linhas_editadas, linhas_alteradas = editar_registros(linhas)

    # Verificar e adicionar os novos registros
    linhas_editadas = verificar_e_adicionar_multiplos_registros(novos_registros, linhas_editadas)

    # Atualizar o registro 0990
    linhas_editadas = atualizar_registro_0990(linhas_editadas)

    # Atualizar o registro 9999
    linhas_editadas = atualizar_registro_9900(linhas_editadas)

    # Atualizar o registro 0500_9900
    linhas_editadas = atualizar_registro_0500_9900(linhas_editadas)


    # Escrita de volta no arquivo
    escrever_arquivo_sped(caminho_arquivo, linhas_editadas)

    # Mostrar as linhas alteradas
    print("Linhas alteradas:")
    for linha in linhas_alteradas:
        print(linha)

    print("Arquivo editado com sucesso!")
else:
    print("Nenhum arquivo foi selecionado.")

    

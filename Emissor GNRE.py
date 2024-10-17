# cpt_n3m0

import datetime
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from unittest import result
import xml.etree.ElementTree as ET
import os
import csv

# Diretórios padrões
#DINATECNICA
#PASTA_ORIGEM_PADRAO = r"C:\Users\Wesley.Raimundo\Desktop\XML"
#PASTA_DESTINO_PADRAO = r"C:\Users\Wesley.Raimundo\Desktop\python\python\Projeto - SPED\Emissor GNRE\XML Retorno"
#CASA
PASTA_ORIGEM_PADRAO = r"I:\python\python\Projeto Gerador de GNRE\XML"
PASTA_DESTINO_PADRAO = r"I:\python\python\Resultado"


# Função auxiliar para obter texto de elementos XML de forma segura
def get_element_text(element, xpath, nsmap, default=''):
    el = element.find(xpath, nsmap)
    return el.text if el is not None else default

# Função para processar os arquivos XML
def processar_arquivos_xml():
    pasta_origem = entrada_origem.get()
    pasta_destino = entrada_destino.get()

    if not pasta_origem or not pasta_destino:
        messagebox.showerror("Erro", "Por favor, selecione as pastas de origem e destino.")
        return

    arquivos_xml = [f for f in os.listdir(pasta_origem) if f.endswith('.xml')]

    barra_progresso['maximum'] = len(arquivos_xml)
    barra_progresso['value'] = 0

    dados_relatorio = []

    for i, nome_arquivo in enumerate(arquivos_xml):
        caminho_arquivo = os.path.join(pasta_origem, nome_arquivo)
        try:
            arvore = ET.parse(caminho_arquivo)
            raiz = arvore.getroot()

            # Extrair dados necessários do XML da NFe
            dados_nfe = extrair_dados_nfe(raiz)
    
    
    # Verificar se as tags vST e vFCPST são diferentes de zero
            if float(dados_nfe['vST'] or 0) == 0 and float(dados_nfe['vFCPST'] or 0) == 0:
                    print(f"Arquivo {nome_arquivo} ignorado: vST e vFCPST são zero.")
                    continue  # Ignora o arquivo e passa para o próximo


            # Gerar XML da GNRE
            xml_gnre = gerar_xml_gnre(dados_nfe)

            # Salvar XML da GNRE
            salvar_xml_gnre(xml_gnre, pasta_destino, nome_arquivo)

            # Adicionar dados ao relatório
            dados_relatorio.append([
                dados_nfe['nNF'],
                dados_nfe['UF'],
                dados_nfe['vST'] or dados_nfe['vICMSUFDest']
            ])

        except Exception as e:
            salvar_log_erro(str(e), nome_arquivo)
            messagebox.showerror("Erro", f"Erro ao processar o arquivo {nome_arquivo}: {str(e)}")

        # Atualiza a barra de progresso
        barra_progresso['value'] = i + 1
        root.update_idletasks()

    # Gerar relatório
    gerar_relatorio(dados_relatorio, pasta_destino)
    messagebox.showinfo("Sucesso", "Processamento concluído. Os arquivos XML da GNRE e o relatório foram gerados.")


def extrair_sped(texto):
    padrao = r'S/PED:\s*(\d+)'
    resultado = re.search(padrao, texto)
    if resultado:
        return resultado.group(1)  # Retorna apenas o número, sem o "S/PED:"
    return ""



# Função para extrair os dados da NFe
def extrair_dados_nfe(raiz):
    nsmap = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
    dados_nfe = {
        'UF': get_element_text(raiz, './/nfe:enderDest/nfe:UF', nsmap),
        'CNPJ': get_element_text(raiz, './/nfe:emit/nfe:CNPJ', nsmap),
        'razaoSocial': get_element_text(raiz, './/nfe:emit/nfe:xNome', nsmap),
        'endereco': get_element_text(raiz, './/nfe:enderEmit/nfe:xLgr', nsmap),
        'municipio': get_element_text(raiz, './/nfe:enderEmit/nfe:cMun', nsmap)[2:],
        'uf': get_element_text(raiz, './/nfe:enderEmit/nfe:UF', nsmap),
        'cep': get_element_text(raiz, './/nfe:enderEmit/nfe:CEP', nsmap),
        'telefone': get_element_text(raiz, './/nfe:enderEmit/nfe:fone', nsmap),
        'receita': get_element_text(raiz, './/nfe:dest/nfe:indIEDest', nsmap),
        'nNF': get_element_text(raiz, './/nfe:ide/nfe:nNF', nsmap),
        'documentoOrigem': raiz.find('.//nfe:infNFe', nsmap).attrib['Id'][3:],
        'vST': get_element_text(raiz, './/nfe:ICMSTot/nfe:vST', nsmap),
        'vICMSUFDest': get_element_text(raiz, './/nfe:ICMSTot/nfe:vICMSUFDest', nsmap),
        'vFCPST': get_element_text(raiz, './/nfe:ICMSTot/nfe:vFCPST', nsmap),
        'IE': get_element_text(raiz, './/nfe:dest/nfe:IE', nsmap),
        'xNome_dest': get_element_text(raiz, './/nfe:dest/nfe:xNome', nsmap),
        'CNPJ_dest': get_element_text(raiz, './/nfe:dest/nfe:CNPJ', nsmap),
        'infAdProd': get_element_text(raiz, './/nfe:det/nfe:infAdProd', nsmap),
    }
    
    return dados_nfe
    
   
    

# Função para gerar o XML GNRE
def gerar_xml_gnre(dados_nfe):
    nsmap = {"gnre": "http://www.gnre.pe.gov.br"}
       
   
    mes_atual = datetime.datetime.now().strftime("%m")  # MM (mês atual)
    ano_atual = datetime.datetime.now().strftime("%Y")  # AAAA (ano atual)
    
    
    data_atual = datetime.datetime.now().strftime("%Y-%m-%d")  # AAAA-MM-DD

    #data_atual = datetime.datetime.now().strftime("%Y-%m-%d")  # AAAA-MM-DD
    #data_elemento = ET.SubElement(item, 'dataAtual')
    #data_elemento.text = data_atual  # Define a data atual no XML

    # Cria a raiz do XML GNRE
    raiz_gnre = ET.Element("TLote_GNRE", xmlns=nsmap["gnre"], versao="2.00")
    sub_raiz_gnre = ET.Element('TDadosGNRE',xmlns=nsmap['gnre'])
    sub_itens = ET.Element("itensGNRE")        
    
        
    # Preenchimento do XML com base nos dados da NFe
    
    
    guias = ET.SubElement(raiz_gnre, "guias")
    TDadosGNRE = ET.SubElement(guias, "TDadosGNRE", versao='2.00')
    
    #guias.text =  'verao '2.00' 
    uf_favorecida = ET.SubElement(TDadosGNRE, "ufFavorecida")
    uf_favorecida.text = dados_nfe['UF']
    tipoGnre = ET.SubElement(TDadosGNRE, "tipoGnre")
    tipoGnre.text = "0"
    
    
    
    #tipoGnre = ET.SubElement(tipoGnre, "0")
    #tipoGnre.text = tipoGnre = [0]
    
    
    
    
    contribuinte_emitente = ET.SubElement(TDadosGNRE, "contribuinteEmitente")
    identificacao = ET.SubElement(contribuinte_emitente, "identificacao")
    cnpj = ET.SubElement(identificacao, "CNPJ")
    cnpj.text = dados_nfe['CNPJ']
    
    identificacao = ET.SubElement(contribuinte_emitente, "razaoSocial")
    identificacao.text = dados_nfe ['razaoSocial'] # type: ignore
    
    
    identificacao = ET.SubElement(contribuinte_emitente, "endereco")
    identificacao.text = dados_nfe ['endereco'] # type: ignore
    
    
    
    identificacao = ET.SubElement(contribuinte_emitente, "municipio")
    identificacao.text = dados_nfe ['municipio'] # type: ignore
    identificacao = ET.SubElement(contribuinte_emitente, "uf")
    identificacao.text = dados_nfe ['uf'] # type: ignore
    identificacao = ET.SubElement(contribuinte_emitente, 'cep')
    identificacao.text = dados_nfe ['cep'] # type: ignore
    identificacao = ET.SubElement(contribuinte_emitente, 'telefone')
    identificacao.text = dados_nfe ['telefone'] # type: ignore
    
    itensGNRE = ET.SubElement(TDadosGNRE, "itensGNRE")
    itensGNRE = ET.SubElement(itensGNRE, "item")
    receita = ET.SubElement(itensGNRE, 'receita')
    receita.text = '100099' if dados_nfe ['receita'] == '1'  else '100120'
     #Lógica condicional por UF
    
    if dados_nfe['UF'] == 'MG': # Cria o elemento 'documentoOrigem' com o atributo 'tipo='10'
        documentoOrigem = ET.SubElement(itensGNRE, "documentoOrigem", tipo="10")
        documentoOrigem.text = dados_nfe['documentoOrigem']  # Aqui estou assumindo que o 'documentoOrigem' será preenchido com o número da nota
    if dados_nfe['UF'] == 'RS': # Cria o elemento 'documentoOrigem' com o atributo 'tipo='22'
        documentoOrigem = ET.SubElement(itensGNRE, "documentoOrigem", tipo="22")
        documentoOrigem.text = dados_nfe['documentoOrigem']  # Aqui estou assumindo que o 'documentoOrigem' será preenchido com o número da nota
    if dados_nfe['UF'] == 'RJ': # Cria o elemento 'documentoOrigem' com o atributo 'tipo='24'
        documentoOrigem = ET.SubElement(itensGNRE, "documentoOrigem", tipo="24")
        documentoOrigem.text = dados_nfe['nNF']  # Aqui estou assumindo que o 'documentoOrigem' será preenchido com o número da nota
    if dados_nfe['UF'] == 'PI': # Cria o elemento 'documentoOrigem' com o atributo 'tipo='24'
        documentoOrigem = ET.SubElement(itensGNRE, "documentoOrigem", tipo="24")
        documentoOrigem.text = dados_nfe['nNF']  # Aqui estou assumindo que o 'documentoOrigem' será preenchido com o número da nota
    if dados_nfe['UF'] == 'AL': # Cria o elemento 'documentoOrigem' com o atributo 'tipo='10'
        documentoOrigem = ET.SubElement(itensGNRE, "documentoOrigem", tipo="10")
        documentoOrigem.text = dados_nfe['nNF']  # Aqui estou assumindo que o 'documentoOrigem' será preenchido com o número da nota    
    if dados_nfe['UF'] == 'RN': # Cria o elemento 'documentoOrigem' com o atributo 'tipo='10'
        documentoOrigem = ET.SubElement(itensGNRE, "documentoOrigem", tipo="10")
        documentoOrigem.text = dados_nfe['nNF']  # Aqui estou assumindo que o 'documentoOrigem' será preenchido com o número da nota    
    if dados_nfe['UF'] == 'BA': # Cria o elemento 'documentoOrigem' com o atributo 'tipo='10'
        documentoOrigem = ET.SubElement(itensGNRE, "documentoOrigem", tipo="10")
        documentoOrigem.text = dados_nfe['nNF']  # Aqui estou assumindo que o 'documentoOrigem' será preenchido com o número da nota    
    if dados_nfe['UF'] == 'CE': # Cria o elemento 'documentoOrigem' com o atributo 'tipo='10'
        documentoOrigem = ET.SubElement(itensGNRE, "documentoOrigem", tipo="10")
        documentoOrigem.text = dados_nfe['nNF']  # Aqui estou assumindo que o 'documentoOrigem' será preenchido com o número da nota    
    if dados_nfe['UF'] == 'DF': # Cria o elemento 'documentoOrigem' com o atributo 'tipo='10'
        documentoOrigem = ET.SubElement(itensGNRE, "documentoOrigem", tipo="10")
        documentoOrigem.text = dados_nfe['nNF']  # Aqui estou assumindo que o 'documentoOrigem' será preenchido com o número da nota    
    if dados_nfe['UF'] == 'ES': # Cria o elemento 'documentoOrigem' com o atributo 'tipo='10'
        documentoOrigem = ET.SubElement(itensGNRE, "documentoOrigem", tipo="10")
        documentoOrigem.text = dados_nfe['nNF']  # Aqui estou assumindo que o 'documentoOrigem' será preenchido com o número da nota    
    if dados_nfe['UF'] == 'CE': # Cria o elemento 'documentoOrigem' com o atributo 'tipo='10'
        documentoOrigem = ET.SubElement(itensGNRE, "documentoOrigem", tipo="10")
        documentoOrigem.text = dados_nfe['nNF']  # Aqui estou assumindo que o 'documentoOrigem' será preenchido com o número da nota    
    if dados_nfe['UF'] == 'AM': # Cria o elemento 'documentoOrigem' com o atributo 'tipo='10'
        documentoOrigem = ET.SubElement(itensGNRE, "documentoOrigem", tipo="10")
        documentoOrigem.text = dados_nfe['nNF']  # Aqui estou assumindo que o 'documentoOrigem' será preenchido com o número da nota    
    if dados_nfe['UF'] == 'PE': # Cria o elemento 'documentoOrigem' com o atributo 'tipo='10'
        documentoOrigem = ET.SubElement(itensGNRE, "documentoOrigem", tipo="22")
        documentoOrigem.text = dados_nfe['nNF']  # Aqui estou assumindo que o 'documentoOrigem' será preenchido com o número da nota    
    if dados_nfe['UF'] == 'MS': # Cria o elemento 'documentoOrigem' com o atributo 'tipo='10'
        documentoOrigem = ET.SubElement(itensGNRE, "documentoOrigem", tipo="10")
        documentoOrigem.text = dados_nfe['nNF']  # Aqui estou assumindo que o 'documentoOrigem' será preenchido com o número da nota    
    if dados_nfe['UF'] == 'MT': # Cria o elemento 'documentoOrigem' com o atributo 'tipo='10'
        documentoOrigem = ET.SubElement(itensGNRE, "documentoOrigem", tipo="10")
        documentoOrigem.text = dados_nfe['nNF']  # Aqui estou assumindo que o 'documentoOrigem' será preenchido com o número da nota    
    if dados_nfe['UF'] == 'GO': # Cria o elemento 'documentoOrigem' com o atributo 'tipo='10'
        documentoOrigem = ET.SubElement(itensGNRE, "documentoOrigem", tipo="10")
        documentoOrigem.text = dados_nfe['nNF']  # Aqui estou assumindo que o 'documentoOrigem' será preenchido com o número da nota    
    if dados_nfe['UF'] == 'PR': # Cria o elemento 'documentoOrigem' com o atributo 'tipo='10'
        documentoOrigem = ET.SubElement(itensGNRE, "documentoOrigem", tipo="10")
        documentoOrigem.text = dados_nfe['nNF']  # Aqui estou assumindo que o 'documentoOrigem' será preenchido com o número da nota    
    if dados_nfe['UF'] == 'SC': # Cria o elemento 'documentoOrigem' com o atributo 'tipo='10'
        documentoOrigem = ET.SubElement(itensGNRE, "documentoOrigem", tipo="10")
        documentoOrigem.text = dados_nfe['nNF']  # Aqui estou assumindo que o 'documentoOrigem' será preenchido com o número da nota    
    if dados_nfe['UF'] == 'SE': # Cria o elemento 'documentoOrigem' com o atributo 'tipo='10'
        documentoOrigem = ET.SubElement(itensGNRE, "documentoOrigem", tipo="10")
        documentoOrigem.text = dados_nfe['nNF']  # Aqui estou assumindo que o 'documentoOrigem' será preenchido com o número da nota    
#    itensGNRE = ET.SubElement(itensGNRE, "item")
    produto = ET.SubElement(itensGNRE, 'produto')
    produto.text = '18'
    referencia = ET.SubElement(itensGNRE, "referencia")
    
    # periodo de apuração
    
    periodo = ET.SubElement(referencia, "periodo")
    periodo.text = '0'
    mes = ET.SubElement(referencia, "mes")
    mes.text = mes_atual
    ano = ET.SubElement(referencia, "ano")
    ano.text = ano_atual
    dataVencimento = ET.SubElement(itensGNRE, 'dataVencimento')
    dataVencimento.text = data_atual
    # periodo de apuração
    
    # Se um dos dois impostos não estiverem preenchidos não será gerada a #TAG#
    if float(dados_nfe['vST']) != 0:
        valor = ET.SubElement(itensGNRE, 'valor', tipo="11")
        valor.text = dados_nfe['vST']
    if float(dados_nfe['vFCPST']) != 0:
        valor = ET.SubElement(itensGNRE, 'valor', tipo="12")
        valor.text = dados_nfe['vFCPST']
    # Se um dos dois impostos não estiverem preenchidos não será gerada a #TAG#
    if dados_nfe['UF'] == 'BA':
        convenio = ET.SubElement(itensGNRE, 'convenio')
        convenio.text = "104/09"
    if dados_nfe['UF'] == 'DF':
        convenio = ET.SubElement(itensGNRE, 'convenio')
        convenio.text = "25/11"
    if dados_nfe['UF'] == 'ES':
        convenio = ET.SubElement(itensGNRE, 'convenio')
        convenio.text = "20/13"
    if dados_nfe['UF'] == 'GO':
        convenio = ET.SubElement(itensGNRE, 'convenio')
        convenio.text = "82/11"
    if dados_nfe['UF'] == 'MG':
        convenio = ET.SubElement(itensGNRE, 'convenio')
        convenio.text = "32/09"
    if dados_nfe['UF'] == 'PE':
        convenio = ET.SubElement(itensGNRE, 'convenio')
        convenio.text = "128/10"
    if dados_nfe['UF'] == 'PR':
        convenio = ET.SubElement(itensGNRE, 'convenio')
        convenio.text = "71/11"
    if dados_nfe['UF'] == 'RJ':
        convenio = ET.SubElement(itensGNRE, 'convenio')
        convenio.text = "32/14"
    if dados_nfe['UF'] == 'RS':
        convenio = ET.SubElement(itensGNRE, 'convenio')
        convenio.text = "92/09"
    contribuinteDestinatario = ET.SubElement(itensGNRE, "contribuinteDestinatario")
    identificacao = ET.SubElement(contribuinteDestinatario, "identificacao")
    IE = ET.SubElement(identificacao, "IE")
    IE.text = dados_nfe['IE']
     
    camposExtras = ET.SubElement(itensGNRE, 'camposExtras')
    campoExtra = ET.SubElement(camposExtras, 'campoExtra')
    if dados_nfe['UF'] == 'SC':
        codigo = ET.SubElement(campoExtra, 'codigo')
        codigo.text = "84"
        campoExtra = ET.SubElement(campoExtra, 'valor')    
        valor.text = data_atual
    if dados_nfe['UF'] == 'PR':
        codigo = ET.SubElement(campoExtra, 'codigo')
        codigo.text = "87"
        campoExtra = ET.SubElement(campoExtra, 'valor')    
        valor.text = data_atual
    if dados_nfe['UF'] == 'SE':
        codigo = ET.SubElement(campoExtra, 'codigo')
        codigo.text = "77"
        campoExtra = ET.SubElement(campoExtra, 'valor')    
        valor.text = data_atual
    if dados_nfe['UF'] == 'BA':
        codigo = ET.SubElement(campoExtra, 'codigo')
        codigo.text = "84"
        campoExtra = ET.SubElement(campoExtra, 'valor')    
        valor.text = data_atual
    if dados_nfe['UF'] == 'DF':
        codigo = ET.SubElement(campoExtra, 'codigo')
        codigo.text = "74"
        campoExtra = ET.SubElement(campoExtra, 'valor')    
        valor.text = data_atual
    if dados_nfe['UF'] == 'GO':
        codigo = ET.SubElement(campoExtra, 'codigo')
        codigo.text = "102"
        campoExtra = ET.SubElement(campoExtra, 'valor')    
        valor.text = data_atual
    if dados_nfe['UF'] == 'MG':
        codigo = ET.SubElement(campoExtra, 'codigo')
        codigo.text = "74"
        campoExtra = ET.SubElement(campoExtra, 'valor')
        valor.text = data_atual
    if dados_nfe['UF'] == 'RS':
        codigo = ET.SubElement(campoExtra, 'codigo')
        codigo.text = "74"
        valor = ET.SubElement(campoExtra, 'valor')    
        valor.text = data_atual
    if dados_nfe['UF'] == 'MA':
        codigo = ET.SubElement(campoExtra, 'codigo')
        codigo.text = "94"
        campoExtra = ET.SubElement(campoExtra, 'valor')    
        valor.text = data_atual
    if dados_nfe['UF'] == 'MT':
        codigo = ET.SubElement(campoExtra, 'codigo')
        codigo.text = "17"
        campoExtra = ET.SubElement(campoExtra, 'valor')    
        valor.text = data_atual
    if dados_nfe['UF'] == 'PE':
        codigo = ET.SubElement(campoExtra, 'codigo')
        codigo.text = "9"
        campoExtra = ET.SubElement(campoExtra, 'valor')    
        valor.text = data_atual
    if dados_nfe['UF'] == 'AL':
        codigo = ET.SubElement(campoExtra, 'codigo')
        codigo.text = "90"
        campoExtra = ET.SubElement(campoExtra, 'valor')    
        valor.text = data_atual
    if dados_nfe['UF'] == 'RJ':
        codigo = ET.SubElement(campoExtra, 'codigo')
        codigo.text = "117"
        campoExtra = ET.SubElement(campoExtra, 'valor')    
        valor.text = data_atual
    if dados_nfe['UF'] == 'PA':
        codigo = ET.SubElement(campoExtra, 'codigo')
        codigo.text = "101"
        campoExtra = ET.SubElement(campoExtra, 'valor')    
        valor.text = data_atual
    if dados_nfe['UF'] == 'CE':
        codigo = ET.SubElement(campoExtra, 'codigo')
        codigo.text = "12"
        campoExtra = ET.SubElement(campoExtra, 'valor')    
        valor.text = data_atual
    if dados_nfe['UF'] == 'DF':
        codigo = ET.SubElement(campoExtra, 'codigo')
        codigo.text = "65"
        campoExtra = ET.SubElement(campoExtra, 'valor')    
        valor.text = data_atual
    if dados_nfe['UF'] == 'MS':
        codigo = ET.SubElement(campoExtra, 'codigo')
        codigo.text = "88"
        campoExtra = ET.SubElement(campoExtra, 'valor')    
        valor.text = data_atual
    if dados_nfe['UF'] == 'GO':
        codigo = ET.SubElement(campoExtra, 'codigo')
        codigo.text = "88"
        campoExtra = ET.SubElement(campoExtra, 'valor')    
        valor.text = data_atual
    #campoExtra = ET.SubElement(campoExtra, 'campoExtra')
    def obter_codigo_uf(uf):
        codigos_uf = {
        "AL": "104/08",
        "BA": "104/09",
        "DF": "25/11",
        "ES": "20/13",
        "GO": "82/11",
        "MG": "32/09",
        "PE": "128/10",
        "PR": "71/11",
        "RJ": "32/14",
        "RS": "92/09",
        "SC": "116/12",
        "SE": "33/12",
        "NC": "93/15",
        "PI": "93/15",
        "CE": "93/15",
        "AP": "60/11"
    }
        return codigos_uf.get(uf, "")
    sped = extrair_sped(dados_nfe['infAdProd'])
    
    
    if dados_nfe['UF'] == 'RS':
        camposExtras = ET.SubElement(camposExtras, 'campoExtra')
        codigo = ET.SubElement(camposExtras, 'codigo')
        codigo.text = "62"
        camposExtras = ET.SubElement(camposExtras, 'valor')    
    camposExtras.text = f"NF-e {dados_nfe['nNF']} {dados_nfe['xNome_dest'].split()[0]} {dados_nfe['CNPJ_dest']} S/PED: {sped}"
         
    valorGNRE = ET.SubElement(TDadosGNRE, "valorGNRE")
    valorGNRE.text = f"{float(dados_nfe['vST']) + float(dados_nfe['vFCPST']):.2f}"
    
    dataPagamento = ET.SubElement(TDadosGNRE, "dataPagamento")
    dataPagamento.text = data_atual

    

    return ET.tostring(raiz_gnre, encoding='unicode')

# Função para salvar o XML GNRE gerado
def salvar_xml_gnre(xml_gnre, pasta_destino, nome_arquivo_original):
    novo_nome_arquivo = f"GNRE_{nome_arquivo_original}"
    caminho_arquivo = os.path.join(pasta_destino, novo_nome_arquivo)
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        f.write(xml_gnre)

# Função para gerar o relatório em CSV
def gerar_relatorio(dados_relatorio, pasta_destino):
    arquivo_relatorio = os.path.join(pasta_destino, "relatorio_gnre.csv")
    with open(arquivo_relatorio, 'w', newline='', encoding='utf-8') as f:
        escritor = csv.writer(f)        
        escritor.writerow(["Número da Nota", "UF", "Valor dos Impostos"])
        escritor.writerows(dados_relatorio)

# Função para salvar logs de erro
def salvar_log_erro(erro, arquivo):
    with open('log_erros.txt', 'a') as f:
        f.write(f"Erro no arquivo {arquivo}: {erro}\n")

# Funções para selecionar pastas
def selecionar_pasta_origem():
    pasta = filedialog.askdirectory()
    if pasta:  # Se o usuário selecionou uma pasta
        entrada_origem.delete(0, tk.END)
        entrada_origem.insert(0, pasta)

def selecionar_pasta_destino():
    pasta = filedialog.askdirectory()
    if pasta:  # Se o usuário selecionou uma pasta
        entrada_destino.delete(0, tk.END)
        entrada_destino.insert(0, pasta)

# Criar janela principal
root = tk.Tk()
root.title("Processador de NFe para GNRE")
root.geometry("600x350")
# Adiciona um estilo customizado

style = ttk.Style()
style.configure("TProgressbar", troughcolor='gray', background='blue', thickness=30)

# Seleção da pasta de origem (com valor padrão)
tk.Label(root, text="Pasta de Origem:").grid(row=0, column=0, padx=5, pady=5)
entrada_origem = tk.Entry(root, width=50)
entrada_origem.grid(row=0, column=1, padx=5, pady=5)
entrada_origem.insert(0, PASTA_ORIGEM_PADRAO)  # Define a pasta padrão
tk.Button(root, text="Procurar", command=selecionar_pasta_origem).grid(row=0, column=2, padx=5, pady=5)

# Seleção da pasta de destino (com valor padrão)
tk.Label(root, text="Pasta de Destino:").grid(row=1, column=0, padx=5, pady=5)
entrada_destino = tk.Entry(root, width=50)
entrada_destino.grid(row=1, column=1, padx=5, pady=5)
entrada_destino.insert(0, PASTA_DESTINO_PADRAO)  # Define a pasta padrão
tk.Button(root, text="Procurar", command=selecionar_pasta_destino).grid(row=1, column=2, padx=5, pady=5)

# Barra de progresso
barra_progresso = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
barra_progresso.grid(row=2, column=1, padx=5, pady=5)

# Botão de processamento
tk.Button(root, text="Processar Arquivos XML", command=processar_arquivos_xml).grid(row=3, column=1, padx=5, pady=20)

# Iniciar a interface gráfica
root.mainloop()
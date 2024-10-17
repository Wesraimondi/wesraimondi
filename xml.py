import pandas as pd
import xml.etree.ElementTree as ET
from tkinter import Tk
from tkinter.filedialog import askopenfilenames

def xml_to_dataframe(xml_files):
    data = []

    for file in xml_files:
        tree = ET.parse(file)
        root = tree.getroot()
        
        # Extraindo informações gerais da nota
        nfe_info = {
            'Chave de Acesso': root.find('.//infNFe/chave').text,
            'Data de Emissão': root.find('.//infNFe/dhEmi').text,
            'CNPJ Emitente': root.find('.//emit/CNPJ').text,
            'Nome Emitente': root.find('.//emit/xNome').text,
            'CNPJ Destinatário': root.find('.//dest/CNPJ').text,
            'Nome Destinatário': root.find('.//dest/xNome').text,
            'Valor Total': root.find('.//ICMSTot/vNF').text,
            'Forma de Pagamento': root.find('.//pag/vTroco').text if root.find('.//pag/vTroco') is not None else 'N/A',
            'Modelo': root.find('.//infNFe/codModelo').text,
            'Série': root.find('.//infNFe/serie').text,
            'Número': root.find('.//infNFe/nNF').text
        }
        
        # Extraindo informações dos itens
        for item in root.findall('.//det'):
            item_info = {6
                'Chave de Acesso': nfe_info['Chave de Acesso'],
                'Data de Emissão': nfe_info['Data de Emissão'],
                'CNPJ Emitente': nfe_info['CNPJ Emitente'],
                'Nome Emitente': nfe_info['Nome Emitente'],
                'CNPJ Destinatário': nfe_info['CNPJ Destinatário'],
                'Nome Destinatário': nfe_info['Nome Destinatário'],
                'Valor Total': nfe_info['Valor Total'],
                'Forma de Pagamento': nfe_info['Forma de Pagamento'],
                'Modelo': nfe_info['Modelo'],
                'Série': nfe_info['Série'],
                'Número': nfe_info['Número'],
                'Produto': item.find('prod/xProd').text,
                'NCM': item.find('prod/NCM').text,
                'CFOP': item.find('prod/CFOP').text,
                'Quantidade': item.find('prod/qCom').text,
                'Valor Unitário': item.find('prod/vUnCom').text,
                'Valor Total do Item': item.find('prod/vProd').text
            }
            data.append(item_info)

    return pd.DataFrame(data)

# Iniciar a interface gráfica para seleção de arquivos
Tk().withdraw()  # Oculta a janela principal
xml_files = askopenfilenames(title='Selecione os arquivos XML', filetypes=[('XML Files', '*.xml')])

if xml_files:
    df = xml_to_dataframe(xml_files)
    # Salvar o DataFrame em um arquivo Excel
    output_file = 'notas_fiscais_completo.xlsx'
    df.to_excel(output_file, index=False)
    print(f'Dados extraídos e salvos em {output_file}')
else:
    print('Nenhum arquivo selecionado.')

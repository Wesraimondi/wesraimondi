import tkinter as tk
from tkinter import filedialog
import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    return chardet.detect(raw_data)['encoding']

def process_sped_file():
    root = tk.Tk()
    root.withdraw()

    input_file = filedialog.askopenfilename(title="Selecione o arquivo SPED para processar")
    if not input_file:
        print("Nenhum arquivo selecionado. Encerrando.")
        return

    file_encoding = detect_encoding(input_file)
    print(f"Codificação detectada: {file_encoding}")

    output_file = input_file.rsplit('.', 1)[0] + '_processado.' + input_file.rsplit('.', 1)[1]

    new_accounts = [
        "|0500|01012009|01|A|5|1.1.10.01.0006|Mercadorias Para Revenda|1.01.03.01.01|62522453000135|",
"|0500|01012009|01|A|5|1.1.20.02.0099|Outros Gastos à  Apropriar|1.01.05.01.09|62522453000135|",
"|0500|01012009|04|A|5|3.1.01.01.0002|Vendas Para Outros Estados|3.01.01.01.01.04|62522453000135|",
"|0500|01012009|01|A|5|1.2.03.06.0006|Empilhadeiras e Guinchos|1.02.03.01.06|62522453000135|",
"|0500|01012009|04|A|5|3.1.01.01.0001|Vendas Para o Estado|3.01.01.01.01.04|62522453000135|",
"|0500|01012009|04|A|5|3.1.01.01.0003|Vendas Para o Exterior|3.01.01.01.01.01|62522453000135|",
"|0500|01012009|04|A|5|3.1.01.01.0004|Revenda de Produtos|3.01.01.01.01.05|62522453000135|",
"|0500|01012009|02|A|5|2.1.01.01.0002|Fornecedores de Serviços|2.01.01.03.01|62522453000135|",
"|0500|01012009|01|A|5|1.1.10.01.0001|Matéria Prima|1.01.03.02.01|62522453000135|",
"|0500|01012009|01|A|5|1.1.10.01.0002|Material Secundário|1.01.03.02.01|62522453000135|",
"|0500|01012009|01|A|5|1.1.10.01.0003|Material de Embalagem|1.01.03.02.02|62522453000135|",
"|0500|01012009|04|A|5|4.1.01.03.0013|Energia Eletrica|3.01.01.03.01.01|62522453000135|",
"|0500|01012009|04|A|5|4.1.01.03.0009|Depreciação de Guincos|3.01.01.03.01.01|62522453000135|",
"|0500|01012009|04|A|5|4.1.01.03.0039|Depreciação de Ferramentas|3.01.01.03.01.01|62522453000135|",
"|0500|01012009|01|A|5|1.1.08.04.0001|Fersa Servs.e Desp.Aduaneiros S/C.Ltda|1.01.02.01.02|62522453000135|",
"|0500|01012009|02|A|5|2.1.02.01.0002|Fornecedores de Outros Serviços|2.01.01.03.01|62522453000135|",
"|0500|01012009|04|A|5|4.1.01.03.0032|Fretes e Carretos|3.01.01.03.01.01|62522453000135|",
"|0500|01012009|05|A|5|5.1.01.02.0032|Fretes e Carretos|3.01.01.07.01.04|62522453000135|",
"|0500|01012009|04|A|5|4.1.01.03.0008|Depreciação Maqs. e Equiptos|3.01.01.03.01.01|62522453000135|",
"|0500|01012009|04|A|5|4.1.01.03.0010|Depreciação de Instalações|3.01.01.03.01.01|62522453000135|",
"|0500|01012009|04|A|5|4.1.01.03.0038|Depreciação de Moveis e Utens|3.01.01.03.01.01|62522453000135|",
"|0500|01012009|04|A|5|4.1.01.03.0064|Depreciação de Hardware|3.01.01.03.01.01|62522453000135|",
"|0500|01012009|04|A|5|4.1.01.03.0041|Locações Diversas|3.01.01.03.01.01|62522453000135|",
"|0500|01012009|04|A|5|3.1.02.01.0001|Juros Ativos|3.01.01.05.01.05|62522453000135|",
"|0500|01012009|04|A|5|3.1.02.01.0002|Descontos obtidos|3.01.01.05.01.05|62522453000135|",
"|0500|01012009|04|A|5|3.1.02.01.0003|Redimento tributos Mercado Aberto|3.01.01.05.01.05|62522453000135|",
"|0500|01012009|04|A|5|3.1.02.02.0003|Variação Cambial Ativas|3.01.01.05.01.01|62522453000135|",
"|0500|01012009|04|A|5|3.1.01.01.0005|Serviços Executados|3.01.01.01.01.06|62522453000135|",
"|0500|01012009|04|A|5|4.1.01.03.00.30|Serviços Tecnicos|3.01.01.03.01.01|62522453000135|",
"|0500|01012009|02|A|5|2.1.02.04.0099|Trânsito valores à Classificar |2.01.01.17.28|62522453000135|",
"|0500|01012009|04|A|5|3.1.01.03.0002|Venda para o Estado|3.01.01.01.04|62522453000135|",
"|0500|01012009|04|A|5|3.1.01.01.0006|Venda de Sucatas|3.01.01.01.01.98|62522453000135|",
"|0500|01012009|02|A|5|2.1.02.04.0099|Valores a Classificar|2.01.01.03.01|62522453000135|",
    ]

    existing_accounts = set()
    lines = []
    in_0500_section = False
    line_count = 0

    try:
        with open(input_file, 'r', encoding=file_encoding, errors='replace') as infile:
            for line in infile:
                line_count += 1
                lines.append(line.strip())
                if line.startswith('|0500|'):
                    in_0500_section = True
                    existing_accounts.add(line.split('|')[2])  # Adiciona o código da conta
                elif line.startswith('|0990|'):
                    if in_0500_section:
                        for account in new_accounts:
                            if account.split('|')[2] not in existing_accounts:
                                lines.insert(-1, account)
                                line_count += 1
                    in_0500_section = False
                elif line.startswith('|9999|'):
                    break

        # Atualiza o registro 0990
        for i, line in enumerate(lines):
            #if line.startswith('|0990|'):
                lines[i] = f"|0990|{line_count}|"
                break

        # Atualiza o registro 9999
        lines[-1] = f"|9999|{line_count}|"

        with open(output_file, 'w', encoding=file_encoding) as outfile:
            for line in lines:
                outfile.write(line + '\n')

        print(f"Processamento concluído. Arquivo de saída: {output_file}")
    except Exception as e:
        print(f"Ocorreu um erro durante o processamento do arquivo: {str(e)}")

if __name__ == "__main__":
    process_sped_file()
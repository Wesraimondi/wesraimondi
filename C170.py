import tkinter as tk
from tkinter import filedialog
import chardet

def process_c170_record(line):
    fields = line.split('|')
    if len(fields) < 38:  # Garantindo que há campos suficientes
        return line  # Retorna a linha original se não tiver campos suficientes

    # Processamento baseado no primeiro dígito do campo 3 [cod_item]
    if fields[3]:
        first_digit = fields[3][0]
        if first_digit == '1':
            fields[37] = '1.1.10.01.0001'
        elif first_digit == '2':
            fields[37] = '1.1.10.01.0002'
        elif first_digit == '3':
            fields[37] = '1.1.10.01.0003'
        elif first_digit == '4':
            fields[37] = '1.1.10.01.0004'
        elif first_digit == '5':
            fields[37] = '1.1.10.01.0005'
        elif first_digit == '6':
            fields[37] = '1.1.10.01.0006'
           # Processamento baseado no campo 11 [CFOP]
    cfop = fields[11]
    if cfop in ['5101', '5102', '5124', '5401']:
        fields[37] = '3.1.01.01.0001'
    elif cfop in ['6102', '6107', '6118', '6401']:
        fields[37] = '3.1.01.01.0002'
    elif cfop == '7101':
        fields[37] = '3.1.01.01.0003'
    elif cfop in ['5102', '6102', '5403', '6403', '6108']:
        fields[37] = '3.1.01.01.0004'
    elif cfop in ['1901', '1902', '2201','2202','1202','1201','5413']:
        fields[37] = '2.1.02.04.0099'
    elif cfop in ['1257', '2257']:
        fields[37] = '4.1.01.03.0013'
    return '|'.join(fields)

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    return chardet.detect(raw_data)['encoding']

def select_and_process_file():
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal

    # Abre o diálogo para selecionar o arquivo de entrada
    input_file = filedialog.askopenfilename(title="Selecione o arquivo SPED para processar")
    
    if not input_file:
        print("Nenhum arquivo selecionado. Encerrando.")
        return

    # Detecta a codificação do arquivo
    file_encoding = detect_encoding(input_file)
    print(f"Codificação detectada: {file_encoding}")

    # Cria o nome do arquivo de saída
    output_file = input_file.rsplit('.', 1)[0] + '_processado_C170.' + input_file.rsplit('.', 1)[1]

    try:
        with open(input_file, 'r', encoding=file_encoding, errors='replace') as infile, \
             open(output_file, 'w', encoding=file_encoding) as outfile:
            for line_number, line in enumerate(infile, start=1):
                try:
                    if line.startswith('|C170|'):
                        processed_line = process_c170_record(line)
                    else:
                        processed_line = line  # Mantém as outras linhas inalteradas
                    outfile.write(processed_line)
                except Exception as e:
                    print(f"Erro ao processar a linha {line_number}: {str(e)}")
                    outfile.write(line)  # Escreve a linha original em caso de erro

        print(f"Processamento concluído. Arquivo de saída: {output_file}")
    except Exception as e:
        print(f"Ocorreu um erro durante o processamento do arquivo: {str(e)}")

if __name__ == "__main__":
    select_and_process_file()
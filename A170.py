import tkinter as tk
from tkinter import filedialog
import chardet
import re

def process_a170_record(line):
    fields = line.split('|')
    if len(fields) < 19:  # Garantindo que há campos suficientes
        return line  # Retorna a linha original se não tiver campos suficientes

    # Processamento baseado no campo 3
    if fields[3]:
        if fields[3].startswith(('09', 'S2', '60')):
            fields[17] = '2.1.01.01.0002'
        elif re.search('[a-zA-Z]', fields[3]):
            fields[17] = '3.1.01.01.0005'

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
    output_file = input_file.rsplit('.', 1)[0] + '_processado_A170.' + input_file.rsplit('.', 1)[1]

    try:
        with open(input_file, 'r', encoding=file_encoding, errors='replace') as infile, \
             open(output_file, 'w', encoding=file_encoding) as outfile:
            for line_number, line in enumerate(infile, start=1):
                try:
                    if line.startswith('|A170|'):
                        processed_line = process_a170_record(line)
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
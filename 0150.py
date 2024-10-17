import tkinter as tk
from tkinter import filedialog

def process_0150_record(line):
    fields = line.split('|')
    if len(fields) < 9:
        return line  # Retorna a linha original se não tiver campos suficientes

    # Verifica o campo 4 [CÓD PAÍS]
    if fields[4] != '1058':
        fields[5] = ''  # Apaga o campo 5 [CNPJ]

    # Verifica o campo 8 [COD MUN]
    if len(fields[8]) >= 2 and fields[8][:2] == '31':
        fields[7] = fields[7].zfill(13)  # Preenche o campo 7 [IE] com zeros à esquerda

    return '|'.join(fields)

def select_and_process_file():
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal

    # Abre o diálogo para selecionar o arquivo de entrada
    input_file = filedialog.askopenfilename(title="Selecione o arquivo SPED para processar")
    
    if not input_file:
        print("Nenhum arquivo selecionado. Encerrando.")
        return

    # Cria o nome do arquivo de saída
    output_file = input_file.rsplit('.', 1)[0] + '_processado.' + input_file.rsplit('.', 1)[1]

    try:
        with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
            for line_number, line in enumerate(infile, start=1):
                try:
                    if line.startswith('|0150|'):
                        processed_line = process_0150_record(line)
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
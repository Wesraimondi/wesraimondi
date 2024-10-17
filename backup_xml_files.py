import os
import shutil
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import time
from ttkbootstrap import Style  # Importando ttkbootstrap para temah

def backup_xml_files():
    # Criar uma janela Tkinter com estilo moderno
    style = Style(theme='flatly')  # Escolha o tema desejado
    root = style.master
    root.title("Backup de XML NFE")
    root.geometry("400x450")

    # Criar a barra de menu
    menubar = tk.Menu(root)

    # Criar o menu "Sobre"
    about_menu = tk.Menu(menubar, tearoff=0)
    about_menu.add_command(label="Sobre", command=lambda: show_about())
    menubar.add_cascade(label="Ajuda", menu=about_menu)

    # Configurar a barra de menu na janela
    root.config(menu=menubar)

    # Criar entradas para diretórios de origem e destino
    tk.Label(root, text="Diretório de origem:").pack(pady=5)
    source_entry = ttk.Entry(root, width=50)
    source_entry.insert(0, r"C:\Users\Wesley.Raimundo\Desktop\XML")
    source_entry.pack(pady=5)

    # Botão para selecionar o diretório de origem
    browse_source_button = ttk.Button(root, text="Selecionar Origem", command=lambda: select_directory(source_entry))
    browse_source_button.pack(pady=5)

    tk.Label(root, text="Diretório de destino:").pack(pady=5)
    dest_entry = ttk.Entry(root, width=50)
    dest_entry.insert(0, r"S:\NFe\2024")
    dest_entry.pack(pady=5)

    # Botão para selecionar o diretório de destino
    browse_dest_button = ttk.Button(root, text="Selecionar Destino", command=lambda: select_directory(dest_entry))
    browse_dest_button.pack(pady=5)

    # Listar meses
    months = [
        ("01 - Janeiro", 1),
        ("02 - Fevereiro", 2),
        ("03 - Março", 3),
        ("04 - Abril", 4),
        ("05 - Maio", 5),
        ("06 - Junho", 6),
        ("07 - Julho", 7),
        ("08 - Agosto", 8),
        ("09 - Setembro", 9),
        ("10 - Outubro", 10),
        ("11 - Novembro", 11),
        ("12 - Dezembro", 12)
    ]

    # Criar uma combobox para selecionar o mês
    month_var = tk.StringVar()
    month_combobox = ttk.Combobox(root, textvariable=month_var, values=[month[0] for month in months], state="readonly")
    month_combobox.pack(pady=20)
    month_combobox.current(0)  # Selecionar o primeiro mês por padrão

    # Criar uma barra de progresso
    progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
    progress.pack(pady=20)

    # Função para iniciar o backup
    def start_backup():
        source_dir = source_entry.get()
        base_dest_dir = dest_entry.get()
        selected_month = month_var.get()
        month_number = next(month[1] for month in months if month[0] == selected_month)

        # Construir o diretório de destino com base no mês escolhido
        dest_dir = os.path.join(base_dest_dir, f"{month_number:02d} - {get_month_name(month_number)}")

        # Verificar se o diretório de destino existe, se não, criar
        os.makedirs(dest_dir, exist_ok=True)

        # Listar arquivos XML no diretório de origem
        xml_files = [file for file in os.listdir(source_dir) if file.endswith('.xml')]
        total_files = len(xml_files)

        if total_files == 0:
            messagebox.showwarning("Aviso", "Nenhum arquivo XML encontrado para copiar.")
            return

        start_time = time.time()
        for idx, file_name in enumerate(xml_files):
            src_file = os.path.join(source_dir, file_name)
            dest_file = os.path.join(dest_dir, file_name)
            shutil.copy2(src_file, dest_file)
            progress['value'] = (idx + 1) / total_files * 100
            root.update_idletasks()  # Atualiza a interface gráfica

        # Excluir arquivos XML do diretório de origem
        for file_name in xml_files:
            os.remove(os.path.join(source_dir, file_name))

        end_time = time.time()
        elapsed_time = end_time - start_time

        messagebox.showinfo("Sucesso", f"Backup realizado com sucesso!\n"
                                        f"Arquivos copiados: {total_files}\n"
                                        f"Tempo total: {elapsed_time:.2f} segundos")

    # Criar um botão para iniciar o backup
    backup_button = ttk.Button(root, text="Iniciar Backup", command=start_backup)
    backup_button.pack(pady=10)

    root.mainloop()

def show_about():
    about_window = tk.Toplevel()
    about_window.title("Sobre")
    about_window.geometry("300x100")
    about_label = tk.Label(about_window, text="Idealizado por Wesley Raimundo", padx=10, pady=10)
    about_label.pack()
    close_button = ttk.Button(about_window, text="Fechar", command=about_window.destroy)
    close_button.pack(pady=5)

def get_month_name(month_number):
    month_names = [
        "Janeiro", "Fevereiro", "Março", "Abril",
        "Maio", "Junho", "Julho", "Agosto",
        "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    return month_names[month_number - 1]

def select_directory(entry):
    selected_directory = filedialog.askdirectory()
    if selected_directory:
        entry.delete(0, tk.END)  # Limpa o campo
        entry.insert(0, selected_directory)  # Insere o diretório selecionado

if __name__ == "__main__":
    backup_xml_files()

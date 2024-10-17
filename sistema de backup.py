import tkinter as tk
from tkinter import filedialog, ttk, scrolledtext
import zipfile
import os
from datetime import datetime
import threading

def backup_pasta(origem, destino, text_widget, progress, status_info):
    try:
        agora = datetime.now().strftime("%d.%m-%Y")
        nome_backup = os.path.join(destino, f"{agora}.zip")
        total_arquivos = sum([len(files) for r, d, files in os.walk(origem)])
        arquivos_processados = 0
        tempo_inicial = datetime.now()

        text_widget.insert(tk.END, "Lendo os arquivos...\n")
        text_widget.yview(tk.END)
        text_widget.update_idletasks()

        with zipfile.ZipFile(nome_backup, 'w', zipfile.ZIP_DEFLATED) as backup_zip:
            for raiz, dirs, files in os.walk(origem):
                for file in files:
                    caminho_completo = os.path.join(raiz, file)
                    backup_zip.write(caminho_completo, os.path.relpath(caminho_completo, origem))
                    arquivos_processados += 1
                    progresso = (arquivos_processados / total_arquivos) * 100
                    tempo_decorrido = (datetime.now() - tempo_inicial).total_seconds()
                    text_widget.insert(tk.END, f"Compactando arquivos...\nProgresso: {progresso:.2f}%\nTempo: {tempo_decorrido:.2f}s\n")
                    text_widget.yview(tk.END)
                    text_widget.update_idletasks()
                    status_info.config(text=f"Arquivos lidos: {arquivos_processados}\nArquivos restantes: {total_arquivos - arquivos_processados}\nTempo: {tempo_decorrido:.2f}s")
        
        tempo_total = (datetime.now() - tempo_inicial).total_seconds()
        text_widget.insert(tk.END, f"Backup completo em {nome_backup}\n")
        text_widget.insert(tk.END, f"Tempo total: {tempo_total:.2f}s\n")
        text_widget.yview(tk.END)
    except Exception as e:
        text_widget.insert(tk.END, f"Erro: {e}\n")
        text_widget.yview(tk.END)

def iniciar_backup():
    origem = filedialog.askdirectory(title="Selecione a pasta de origem")
    if origem:
        destino = filedialog.askdirectory(title="Selecione a pasta de destino")
        if destino:
            text_widget.insert(tk.END, "Iniciando backup...\n")
            text_widget.yview(tk.END)
            thread = threading.Thread(target=backup_pasta, args=(origem, destino, text_widget, progress, status_info))
            thread.start()

root = tk.Tk()
root.title("Sistema de Backup")

style = ttk.Style(root)
style.theme_use('clam')
style.configure('TButton', font=('MS Sans Serif', 10), borderwidth=1)
style.map('TButton', 
          foreground=[('pressed', 'black'), ('active', 'black')],
          background=[('pressed', '!disabled', 'lightgrey'), ('active', 'white')])

# Menu
menu_bar = tk.Menu(root)
backup_menu = tk.Menu(menu_bar, tearoff=0)
backup_menu.add_command(label="Iniciar Backup", command=iniciar_backup)
menu_bar.add_cascade(label="Backup", menu=backup_menu)
root.config(menu=menu_bar)

# Adicionar ícones
# Substitua "caminho_para_o_icone" pelos caminhos reais dos seus ícones
icone_backup = tk.PhotoImage(file="C:/Users/Gamer/Downloads/xml.png")
icone_data_hora = tk.PhotoImage(file="C:/Users/Gamer/Downloads/xml.png")

# Data e hora
data_hora_frame = tk.Frame(root)
data_hora_frame.pack(pady=5)
data_hora_label = ttk.Label(data_hora_frame, text=datetime.now().strftime("%d/%m/%Y %H:%M:%S"), font=('MS Sans Serif', 10))
data_hora_icon = tk.Label(data_hora_frame, image=icone_data_hora)
data_hora_icon.pack(side=tk.LEFT, padx=5)
data_hora_label.pack(side=tk.LEFT)

# Tempo de conclusão, arquivos lidos/restantes
status_info = ttk.Label(root, text="", font=('MS Sans Serif', 10))
status_info.pack(pady=5)

# Texto com aparência MS-DOS
text_frame = tk.Frame(root, bg='black')
text_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
text_widget = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, width=80, height=20, bg='black', fg='green', insertbackground='green', font=('Courier', 10))
text_widget.pack(fill=tk.BOTH, expand=True)

root.mainloop()

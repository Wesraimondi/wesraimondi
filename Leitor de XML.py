import tkinter as tk
from tkinter import filedialog, messagebox, Menu, ttk
import xml.etree.ElementTree as ET
from xml.dom import minidom
import difflib

class XMLEditorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Leitor, Editor e Comparador de XML")
        self.master.geometry("1000x700")

        self.files = {}
        self.current_file = None

        self.create_menu()
        self.create_widgets()
        self.create_notepad()

    def create_menu(self):
        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        file_menu.add_command(label="Abrir XML", command=self.open_file)
        file_menu.add_command(label="Salvar XML", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Comparar XMLs", command=self.compare_xmls)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.master.quit)

    def create_widgets(self):
        # Notebook para abas de arquivos
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

    def create_notepad(self):
        notepad_frame = tk.Frame(self.notebook)
        self.notebook.add(notepad_frame, text="Bloco de Notas")

        # Text widget para números de linha do bloco de notas
        self.notepad_line_numbers = tk.Text(notepad_frame, width=4, padx=3, pady=3, bg='lightgrey', state='disabled')
        self.notepad_line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        # Text widget para o bloco de notas
        self.notepad = tk.Text(notepad_frame, wrap=tk.NONE, padx=3, pady=3)
        self.notepad.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # Scrollbars para o bloco de notas
        notepad_y_scrollbar = tk.Scrollbar(notepad_frame, orient=tk.VERTICAL)
        notepad_y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        notepad_y_scrollbar.config(command=self.sync_notepad_scroll)

        notepad_x_scrollbar = tk.Scrollbar(notepad_frame, orient=tk.HORIZONTAL)
        notepad_x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        notepad_x_scrollbar.config(command=self.notepad.xview)

        self.notepad.config(yscrollcommand=notepad_y_scrollbar.set, xscrollcommand=notepad_x_scrollbar.set)
        self.notepad_line_numbers.config(yscrollcommand=notepad_y_scrollbar.set)

        # Bind events para o bloco de notas
        self.notepad.bind('&lt;Key>', self.update_notepad_line_numbers)
        self.notepad.bind('&lt;MouseWheel>', self.update_notepad_line_numbers)

        # Inicializar números de linha do bloco de notas
        self.update_notepad_line_numbers()

    def sync_notepad_scroll(self, *args):
        self.notepad_line_numbers.yview_moveto(args[1])
        self.notepad.yview_moveto(args[1])

    def update_notepad_line_numbers(self, event=None):
        line_count = self.notepad.get('1.0', tk.END).count('\n')
        line_number_content = '\n'.join(str(i) for i in range(1, line_count + 1))
        self.notepad_line_numbers.config(state='normal')
        self.notepad_line_numbers.delete('1.0', tk.END)
        self.notepad_line_numbers.insert('1.0', line_number_content)
        self.notepad_line_numbers.config(state='disabled')

    def open_file(self):
        filename = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if filename:
            try:
                tree = ET.parse(filename)
                xml_string = self.prettify(tree.getroot())
                
                new_tab = tk.Frame(self.notebook)
                new_editor = self.create_editor_widget(new_tab)
                new_editor.insert(tk.END, xml_string)
                
                self.notebook.add(new_tab, text=filename.split("/")[-1])
                self.notebook.select(new_tab)
                
                self.files[filename] = new_editor
                self.current_file = filename
                
                self.update_line_numbers(new_editor)
            except ET.ParseError as e:
                messagebox.showerror("Erro", f"Erro ao parsear o arquivo XML: {str(e)}")

    def create_editor_widget(self, parent):
        editor_frame = tk.Frame(parent)
        editor_frame.pack(expand=True, fill=tk.BOTH)

        line_numbers = tk.Text(editor_frame, width=4, padx=3, pady=3, bg='lightgrey', state='disabled')
        line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        editor = tk.Text(editor_frame, wrap=tk.NONE, padx=3, pady=3)
        editor.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        y_scrollbar = tk.Scrollbar(editor_frame, orient=tk.VERTICAL)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        y_scrollbar.config(command=lambda *args: self.sync_scroll(editor, line_numbers, *args))

        x_scrollbar = tk.Scrollbar(parent, orient=tk.HORIZONTAL)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        x_scrollbar.config(command=editor.xview)

        editor.config(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        line_numbers.config(yscrollcommand=y_scrollbar.set)

        editor.bind('&lt;Key>', lambda event: self.update_line_numbers(editor))
        editor.bind('&lt;MouseWheel>', lambda event: self.update_line_numbers(editor))

        return editor

    def sync_scroll(self, editor, line_numbers, *args):
        line_numbers.yview_moveto(args[1])
        editor.yview_moveto(args[1])

    def update_line_numbers(self, editor):
        line_numbers = editor.master.winfo_children()[0]  # Assume que o widget de números de linha é o primeiro filho
        line_count = editor.get('1.0', tk.END).count('\n')
        line_number_content = '\n'.join(str(i) for i in range(1, line_count + 1))
        line_numbers.config(state='normal')
        line_numbers.delete('1.0', tk.END)
        line_numbers.insert('1.0', line_number_content)
        line_numbers.config(state='disabled')

    def save_file(self):
        if self.current_file:
            try:
                xml_content = self.files[self.current_file].get(1.0, tk.END)
                root = ET.fromstring(xml_content)
                tree = ET.ElementTree(root)
                tree.write(self.current_file, encoding="utf-8", xml_declaration=True)
                messagebox.showinfo("Sucesso", "Arquivo XML salvo com sucesso!")
            except ET.ParseError as e:
                messagebox.showerror("Erro", f"XML inválido: {str(e)}")
        else:
            messagebox.showwarning("Aviso", "Nenhum arquivo aberto para salvar.")

    def compare_xmls(self):
        if len(self.files) < 2:
            messagebox.showwarning("Aviso", "Abra pelo menos dois arquivos XML para comparar.")
            return
        
        files_to_compare = list(self.files.keys())
        if len(files_to_compare) > 2:
            # Aqui você pode implementar uma caixa de diálogo para selecionar quais arquivos comparar
            # Por simplicidade, vamos apenas pegar os dois primeiros
            files_to_compare = files_to_compare[:2]
        
        xml1 = self.files[files_to_compare[0]].get(1.0, tk.END).splitlines()
        xml2 = self.files[files_to_compare[1]].get(1.0, tk.END).splitlines()
        
        diff = list(difflib.unified_diff(xml1, xml2, fromfile=files_to_compare[0], tofile=files_to_compare[1]))
        
        diff_window = tk.Toplevel(self.master)
        diff_window.title("Comparação de XMLs")
        diff_window.geometry("800x600")
        
        diff_text = tk.Text(diff_window, wrap=tk.NONE)
        diff_text.pack(expand=True, fill=tk.BOTH)
        
        for line in diff:
            if line.startswith('+'):
                diff_text.insert(tk.END, line + '\n', 'green')
            elif line.startswith('-'):
                diff_text.insert(tk.END, line + '\n', 'red')
            else:
                diff_text.insert(tk.END, line + '\n')
        
        diff_text.tag_config('green', foreground='green')
        diff_text.tag_config('red', foreground='red')

    def prettify(self, elem):
        """Retorna uma string XML formatada bonita."""
        rough_string = ET.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

if __name__ == "__main__":
    root = tk.Tk()
    app = XMLEditorApp(root)
    root.mainloop()
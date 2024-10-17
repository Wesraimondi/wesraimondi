import tkinter as tk
from tkinter import ttk
import subprocess
import os

class ProgramaPrincipal:
    def __init__(self):
        self.janela_principal = tk.Tk()
        self.janela_principal.title("Meu Programa")
        self.janela_principal.geometry("400x300")

        self.criar_menu_suspenso()
        self.criar_outros_componentes()

    def criar_menu_suspenso(self):
        self.programas = {
            "Bloco de Notas": "notepad.exe",
            "Calculadora": "calc.exe",
            "Paint": "mspaint.exe"
        }

        frame_menu = ttk.Frame(self.janela_principal)
        frame_menu.pack(pady=10)

        label = ttk.Label(frame_menu, text="Abrir programa:")
        label.pack(side=tk.LEFT, padx=5)

        self.combo = ttk.Combobox(frame_menu, values=list(self.programas.keys()))
        self.combo.pack(side=tk.LEFT, padx=5)
        self.combo.bind("<<ComboboxSelected>>", self.abrir_programa_selecionado)

    def criar_outros_componentes(self):
        # Adicione aqui outros componentes do seu programa principal
        ttk.Label(self.janela_principal, text="Seu programa principal aqui").pack(pady=20)
        ttk.Button(self.janela_principal, text="Outra Função", command=self.outra_funcao).pack()

    def abrir_programa_selecionado(self, event):
        selecionado = self.combo.get()
        if selecionado in self.programas:
            try:
                subprocess.Popen(self.programas[selecionado])
            except FileNotFoundError:
                print(f"Programa não encontrado: {self.programas[selecionado]}")

    def outra_funcao(self):
        print("Outra função do programa principal")

    def executar(self):
        self.janela_principal.mainloop()

if __name__ == "__main__":
    programa = ProgramaPrincipal()
    programa.executar()
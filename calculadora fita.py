import tkinter as tk
from tkinter import messagebox, scrolledtext

class CalculadoraFita:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Fita")

        self.fita = []

        # Tela de entrada
        self.entrada = tk.Entry(self.root, width=20, font=("Arial", 16))
        self.entrada.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        self.entrada.bind('<Return>', self.calcular)  # Bind para a tecla Enter

        # Botões de operação
        self.criar_botoes()

        # Área de texto para mostrar a fita
        self.fita_texto = scrolledtext.ScrolledText(self.root, width=30, height=10, font=("Arial", 12))
        self.fita_texto.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

    def criar_botoes(self):
        botoes = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('+', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('*', 3, 3),
            ('0', 4, 0), ('C', 4, 1), ('/', 4, 2), ('=', 4, 3),
        ]

        for (texto, linha, coluna) in botoes:
            if texto == 'C':
                tk.Button(self.root, text=texto, width=5, height=2, command=self.limpar).grid(row=linha, column=coluna)
            elif texto == '=':
                tk.Button(self.root, text=texto, width=5, height=2, command=self.calcular).grid(row=linha, column=coluna)
            else:
                tk.Button(self.root, text=texto, width=5, height=2, command=lambda t=texto: self.adicionar(t)).grid(row=linha, column=coluna)

    def adicionar(self, valor):
        self.entrada.insert(tk.END, valor)
        self.atualizar_fita()  # Atualiza a fita sempre que um botão é pressionado

    def limpar(self):
        self.entrada.delete(0, tk.END)
        self.fita_texto.delete(1.0, tk.END)  # Limpa a fita

    def atualizar_fita(self):
        expressao = self.entrada.get()
        if expressao:
            self.fita_texto.delete(1.0, tk.END)  # Limpa a área de texto
            self.fita_texto.insert(tk.END, "\n".join(self.fita) + "\n" + expressao)  # Mostra a fita atualizada

    def calcular(self, event=None):  # Recebe o evento como argumento
        expressao = self.entrada.get()
        try:
            resultado = eval(expressao)
            self.fita.append(f"{expressao} = {resultado}")
            self.fita_texto.delete(1.0, tk.END)  # Limpa a área de texto
            self.fita_texto.insert(tk.END, "\n".join(self.fita))  # Mostra a fita atualizada
            self.entrada.delete(0, tk.END)
            self.entrada.insert(tk.END, str(resultado))  # Mostra o resultado na entrada
        except Exception as e:
            messagebox.showerror("Erro", "Entrada inválida!")
            self.limpar()  # Limpa a entrada em caso de erro

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraFita(root)
    root.mainloop()

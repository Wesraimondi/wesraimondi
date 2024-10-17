import tkinter as tk
from tkinter import messagebox

# Função para verificar o login
def verificar_login():
    usuario = entrada_usuario.get()
    senha = entrada_senha.get()
    
    if usuario == "Wesley_raimundo" and senha == "210769":
        messagebox.showinfo("Login", "Login bem-sucedido!")
        # Aqui você pode chamar a função ou parte do código que deseja executar após o login
    else:
        messagebox.showerror("Login", "Usuário ou senha incorretos.")

# Criando a janela principal
janela = tk.Tk()
janela.title("Tela de Login")

# Criando os widgets
label_usuario = tk.Label(janela, text="Usuário:")
label_usuario.pack(pady=5)

entrada_usuario = tk.Entry(janela)
entrada_usuario.pack(pady=5)

label_senha = tk.Label(janela, text="Senha:")
label_senha.pack(pady=5)

entrada_senha = tk.Entry(janela, show="*")
entrada_senha.pack(pady=5)

botao_login = tk.Button(janela, text="Login", command=verificar_login)
botao_login.pack(pady=20)

# Iniciando o loop principal da interface
janela.mainloop()

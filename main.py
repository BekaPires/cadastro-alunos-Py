import tkinter as tk
from tkinter import messagebox
from aluno import janela_aluno
from disciplina import janela_disciplina
from nota import centralizar_janela, janela_nota
import banco  

def main():
    root = tk.Tk()
    root.title("Sistema de Cadastro Escolar")
    root.geometry("400x300")
    root.configure(bg="#f0f8ff")

    centralizar_janela(root, 600, 400)

    # Controle de tela cheia
    def toggle_fullscreen(event=None):
        root.attributes("-fullscreen", not root.attributes("-fullscreen"))

    def end_fullscreen(event=None):
        root.attributes("-fullscreen", False)

    root.bind("<F11>", toggle_fullscreen)
    root.bind("<Escape>", end_fullscreen)

    titulo = tk.Label(root, text="Sistema de Cadastro", font=("Helvetica", 18, "bold"), bg="#f0f8ff", fg="#003366")
    titulo.pack(pady=20)

    btn_aluno = tk.Button(root, text="Gerenciar Alunos", width=25, height=2, bg="#4caf50", fg="white",
                          font=("Helvetica", 12, "bold"), activebackground="#45a049", cursor="hand2",
                          command=janela_aluno)
    btn_aluno.pack(pady=5)

    btn_disciplina = tk.Button(root, text="Gerenciar Disciplinas", width=25, height=2, bg="#2196f3", fg="white",
                               font=("Helvetica", 12, "bold"), activebackground="#1976d2", cursor="hand2",
                               command=janela_disciplina)
    btn_disciplina.pack(pady=5)

    btn_nota = tk.Button(root, text="Gerenciar Notas", width=25, height=2, bg="#ff9800", fg="white",
                         font=("Helvetica", 12, "bold"), activebackground="#fb8c00", cursor="hand2",
                         command=janela_nota)
    btn_nota.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()

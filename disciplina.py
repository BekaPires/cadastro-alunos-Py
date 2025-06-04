import tkinter as tk
from tkinter import ttk, messagebox
from banco import conectar

def janela_disciplina():
    janela = tk.Toplevel()
    janela.title("Gerenciar Disciplinas")
    janela.configure(bg="#f0f8ff")
    janela.resizable(True, True)

    def centralizar_janela(win, largura=600, altura=400):
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        x = (screen_width - largura) // 2
        y = (screen_height - altura) // 2
        win.geometry(f"{largura}x{altura}+{x}+{y}")

    centralizar_janela(janela, 710, 400)

    def limpar_campos():
        id_disciplina.delete(0, tk.END)
        nome.delete(0, tk.END)
        turno.set("Selecione")
        sala.delete(0, tk.END)
        professor.delete(0, tk.END)

    def incluir():
        if not nome.get().strip() or turno.get() == "Selecione":
            messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios!")
            return
        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("INSERT INTO disciplina (nome, turno, sala, professor) VALUES (?, ?, ?, ?)",
                        (nome.get(), turno.get(), sala.get(), professor.get()))
            conn.commit()
            messagebox.showinfo("Sucesso", "Disciplina incluída com sucesso!")
            limpar_campos()
            listar()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao incluir disciplina: {e}")
        finally:
            conn.close()

    def listar():
        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("SELECT * FROM disciplina")
            resultado = cur.fetchall()
            texto.delete("1.0", tk.END)
            cabecalho = f"{'ID':^5} | {'Nome':^30} | {'Turno':^12} | {'Sala':^8} | {'Professor':^20}\n"
            texto.insert(tk.END, cabecalho)
            texto.insert(tk.END, "-" * 85 + "\n")
            for linha in resultado:
                id_val, nome_val, turno_val, sala_val, prof_val = linha
                linha_formatada = f"{str(id_val):^5} | {nome_val:^30} | {turno_val:^12} | {sala_val:^8} | {prof_val:^20}\n"
                texto.insert(tk.END, linha_formatada)
                texto.insert(tk.END, "-" * 85 + "\n")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar disciplinas: {e}")
        finally:
            conn.close()

    def alterar():
        if not id_disciplina.get().strip():
            messagebox.showwarning("Atenção", "Informe o ID para alterar.")
            return
        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("UPDATE disciplina SET nome=?, turno=?, sala=?, professor=? WHERE id=?",
                        (nome.get(), turno.get(), sala.get(), professor.get(), id_disciplina.get()))
            if cur.rowcount == 0:
                messagebox.showwarning("Aviso", "ID não encontrado para alteração.")
            else:
                conn.commit()
                messagebox.showinfo("Sucesso", "Disciplina alterada!")
                limpar_campos()
                listar()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao alterar disciplina: {e}")
        finally:
            conn.close()

    def excluir():
        if not id_disciplina.get().strip():
            messagebox.showwarning("Atenção", "Informe o ID para excluir.")
            return
        if messagebox.askyesno("Confirmação", "Deseja realmente excluir esta disciplina?"):
            try:
                conn = conectar()
                cur = conn.cursor()
                cur.execute("DELETE FROM disciplina WHERE id=?", (id_disciplina.get(),))
                if cur.rowcount == 0:
                    messagebox.showwarning("Aviso", "ID não encontrado para exclusão.")
                else:
                    conn.commit()
                    messagebox.showinfo("Sucesso", "Disciplina excluída!")
                    limpar_campos()
                    listar()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir disciplina: {e}")
            finally:
                conn.close()

    # Layout dos campos
    tk.Label(janela, text="ID", bg="#f0f8ff").grid(row=0, column=0, sticky="e", padx=10, pady=5)
    tk.Label(janela, text="Nome", bg="#f0f8ff").grid(row=1, column=0, sticky="e", padx=10, pady=5)
    tk.Label(janela, text="Turno", bg="#f0f8ff").grid(row=2, column=0, sticky="e", padx=10, pady=5)
    tk.Label(janela, text="Sala", bg="#f0f8ff").grid(row=3, column=0, sticky="e", padx=10, pady=5)
    tk.Label(janela, text="Professor", bg="#f0f8ff").grid(row=4, column=0, sticky="e", padx=10, pady=5)

    id_disciplina = tk.Entry(janela)
    nome = tk.Entry(janela)
    turno = ttk.Combobox(janela, values=["Matutino", "Vespertino", "Noturno"], state="readonly")
    turno.set("Selecione")
    sala = tk.Entry(janela)
    professor = tk.Entry(janela)

    id_disciplina.grid(row=0, column=1, padx=10, pady=5, sticky="we")
    nome.grid(row=1, column=1, padx=10, pady=5, sticky="we")
    turno.grid(row=2, column=1, padx=10, pady=5, sticky="we")
    sala.grid(row=3, column=1, padx=10, pady=5, sticky="we")
    professor.grid(row=4, column=1, padx=10, pady=5, sticky="we")

    # Botões
    frame_botoes = tk.Frame(janela, bg="#f0f8ff")
    frame_botoes.grid(row=5, column=0, columnspan=2, pady=10)

    botoes = [
        ("Incluir", incluir, "#4caf50"),
        ("Alterar", alterar, "#2196f3"),
        ("Excluir", excluir, "#f44336"),
        ("Listar", listar, "#ff9800")
    ]

    for i, (texto_btn, comando, cor) in enumerate(botoes):
        tk.Button(frame_botoes, text=texto_btn, command=comando, bg=cor, fg="white",
                  font=("Helvetica", 10, "bold"), width=10).grid(row=0, column=i, padx=5)

    # Área de texto e scroll
    texto = tk.Text(janela, height=12, width=70, bg="white", wrap="none", font=("Courier New", 10))
    texto.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

    scroll_x = tk.Scrollbar(janela, orient=tk.HORIZONTAL, command=texto.xview)
    scroll_x.grid(row=7, column=0, columnspan=2, sticky="ew")
    texto.configure(xscrollcommand=scroll_x.set)

    janela.grid_rowconfigure(6, weight=1)
    janela.grid_columnconfigure(1, weight=1)

    listar()

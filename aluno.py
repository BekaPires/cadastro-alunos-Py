import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from banco import conectar

def janela_aluno():
    janela = tk.Toplevel()
    janela.title("Gerenciar Alunos")
    janela.configure(bg="#f0f8ff")
    janela.resizable(True, True)  # janela redimensionável

    # Função para centralizar a janela
    def centralizar_janela(win, largura=600, altura=400):
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        x = (screen_width - largura) // 2
        y = (screen_height - altura) // 2
        win.geometry(f"{largura}x{altura}+{x}+{y}")

    centralizar_janela(janela, 750, 400)  

    def validar_campos():
        if not nome.get().strip():
            messagebox.showwarning("Atenção", "Nome é obrigatório!")
            return False
        if not data_nasc.get().strip():
            messagebox.showwarning("Atenção", "Data de Nascimento é obrigatória!")
            return False
        entrada = data_nasc.get().strip().replace("/", "")
        if len(entrada) != 8 or not entrada.isdigit():
            messagebox.showerror("Erro", "Data inválida! Digite no formato DD/MM/AAAA.")
            return False
        try:
            data_formatada = f"{entrada[4:]}-{entrada[2:4]}-{entrada[0:2]}"
            datetime.strptime(data_formatada, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Erro", "Data inválida! Digite no formato DD/MM/AAAA.")
            return False
        return True

    def limpar_campos():
        matricula.delete(0, tk.END)
        nome.delete(0, tk.END)
        data_nasc.delete(0, tk.END)

    def aplicar_mascara_data(event):
        texto = data_nasc.get().replace("/", "")
        novo_texto = ""
        if len(texto) > 0:
            novo_texto += texto[:2]
        if len(texto) > 2:
            novo_texto += "/" + texto[2:4]
        if len(texto) > 4:
            novo_texto += "/" + texto[4:8]
        data_nasc.delete(0, tk.END)
        data_nasc.insert(0, novo_texto)

    def incluir():
        if not validar_campos():
            return
        try:
            entrada = data_nasc.get().strip().replace("/", "")
            data_formatada = f"{entrada[4:]}-{entrada[2:4]}-{entrada[0:2]}"

            conn = conectar()
            cur = conn.cursor()
            cur.execute("INSERT INTO aluno (nome, data_nascimento) VALUES (?, ?)",
                        (nome.get(), data_formatada))
            conn.commit()
            messagebox.showinfo("Sucesso", "Aluno incluído com sucesso!")
            limpar_campos()
            listar()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao incluir aluno: {e}")
        finally:
            conn.close()

    def listar():
        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("SELECT * FROM aluno")
            resultado = cur.fetchall()
            texto.delete("1.0", tk.END)

            # Cabeçalho centralizado com colunas largas
            cabecalho = f"{'Matrícula':^25} | {'Nome':^40} | {'Data Nasc.':^15}\n"
            texto.insert(tk.END, cabecalho)
            texto.insert(tk.END, "-" * 90 + "\n")

            for linha in resultado:
                matricula_val, nome_aluno, data_nasc_val = linha
                data_formatada = datetime.strptime(data_nasc_val, "%Y-%m-%d").strftime("%d/%m/%Y")
                linha_formatada = f"{str(matricula_val):^25} | {nome_aluno:^40} | {data_formatada:^15}\n"
                texto.insert(tk.END, linha_formatada)
                texto.insert(tk.END, "-" * 90 + "\n")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar alunos: {e}")
        finally:
            conn.close()


    def alterar():
        if not validar_campos():
            return
        try:
            entrada = data_nasc.get().strip().replace("/", "")
            data_formatada = f"{entrada[4:]}-{entrada[2:4]}-{entrada[0:2]}"

            conn = conectar()
            cur = conn.cursor()
            cur.execute("UPDATE aluno SET nome=?, data_nascimento=? WHERE matricula=?",
                        (nome.get(), data_formatada, matricula.get()))
            if cur.rowcount == 0:
                messagebox.showwarning("Aviso", "Matrícula não encontrada para alterar.")
            else:
                conn.commit()
                messagebox.showinfo("Sucesso", "Aluno alterado!")
                limpar_campos()
                listar()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao alterar aluno: {e}")
        finally:
            conn.close()

    def excluir():
        if not matricula.get().strip():
            messagebox.showwarning("Atenção", "Informe a matrícula para excluir.")
            return
        if messagebox.askyesno("Confirmação", "Deseja realmente excluir este aluno?"):
            try:
                conn = conectar()
                cur = conn.cursor()
                cur.execute("DELETE FROM aluno WHERE matricula=?", (matricula.get(),))
                if cur.rowcount == 0:
                    messagebox.showwarning("Aviso", "Matrícula não encontrada para exclusão.")
                else:
                    conn.commit()
                    messagebox.showinfo("Sucesso", "Aluno excluído!")
                    limpar_campos()
                    listar()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir aluno: {e}")
            finally:
                conn.close()

    # Layout dos Labels e Entrys
    tk.Label(janela, text="Matrícula", bg="#f0f8ff").grid(row=0, column=0, sticky="e", padx=10, pady=5)
    tk.Label(janela, text="Nome", bg="#f0f8ff").grid(row=1, column=0, sticky="e", padx=10, pady=5)
    tk.Label(janela, text="Data de Nascimento", bg="#f0f8ff").grid(row=2, column=0, sticky="e", padx=10, pady=5)

    matricula = tk.Entry(janela)
    nome = tk.Entry(janela)
    data_nasc = tk.Entry(janela)
    data_nasc.bind("<KeyRelease>", aplicar_mascara_data)

    matricula.grid(row=0, column=1, padx=10, pady=5, sticky="we")
    nome.grid(row=1, column=1, padx=10, pady=5, sticky="we")
    data_nasc.grid(row=2, column=1, padx=10, pady=5, sticky="we")

    # Frame para os botões, alinhados horizontalmente, igual janela notas
    frame_botoes = tk.Frame(janela, bg="#f0f8ff")
    frame_botoes.grid(row=3, column=0, columnspan=2, pady=10)

    botoes = [
        ("Incluir", incluir, "#4caf50"),
        ("Alterar", alterar, "#2196f3"),
        ("Excluir", excluir, "#f44336"),
        ("Listar", listar, "#ff9800")
    ]

    for i, (texto_btn, comando, cor) in enumerate(botoes):
        tk.Button(frame_botoes, text=texto_btn, command=comando, bg=cor, fg="white",
                  font=("Helvetica", 10, "bold"), width=10).grid(row=0, column=i, padx=5)

    # Área de texto para listar os alunos, com scroll horizontal
    texto = tk.Text(janela, height=12, width=70, bg="white", wrap="none", font=("Courier New", 10))
    texto.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

    scroll_x = tk.Scrollbar(janela, orient=tk.HORIZONTAL, command=texto.xview)
    scroll_x.grid(row=5, column=0, columnspan=2, sticky="ew")
    texto.configure(xscrollcommand=scroll_x.set)

    # Configura o grid para crescer o texto junto com janela redimensionável
    janela.grid_rowconfigure(4, weight=1)
    janela.grid_columnconfigure(1, weight=1)

    listar()

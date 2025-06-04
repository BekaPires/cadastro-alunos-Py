import tkinter as tk
from tkinter import ttk, messagebox
from banco import conectar

def centralizar_janela(janela, largura=600, altura=400):
    tela_largura = janela.winfo_screenwidth()
    tela_altura = janela.winfo_screenheight()
    x = (tela_largura - largura) // 2
    y = (tela_altura - altura) // 2
    janela.geometry(f"{largura}x{altura}+{x}+{y}")

def janela_nota():
    janela = tk.Toplevel()
    janela.title("Gerenciar Notas")
    janela.configure(bg="#f0f8ff")
    janela.resizable(True, True)
    centralizar_janela(janela, 600, 400)

    def limpar_campos():
        id_nota.delete(0, tk.END)
        cb_aluno.set('')
        cb_disciplina.set('')
        entrada_nota.delete(0, tk.END)

    def carregar_alunos():
        conn = conectar()
        cur = conn.cursor()
        cur.execute("SELECT matricula, nome FROM aluno")
        dados = [f"{m} - {n}" for m, n in cur.fetchall()]
        conn.close()
        return dados

    def carregar_disciplinas():
        conn = conectar()
        cur = conn.cursor()
        cur.execute("SELECT id, nome FROM disciplina")
        dados = [f"{i} - {n}" for i, n in cur.fetchall()]
        conn.close()
        return dados

    def obter_ids():
        aluno_id = cb_aluno.get().split(" - ")[0]
        disc_id = cb_disciplina.get().split(" - ")[0]
        return aluno_id, disc_id

    def validar_campos():
        try:
            float(entrada_nota.get())
            int(obter_ids()[0])
            int(obter_ids()[1])
            return True
        except:
            messagebox.showwarning("Erro", "Preencha todos os campos corretamente.")
            return False

    def incluir():
        if not validar_campos():
            return
        aluno_id, disc_id = obter_ids()
        conn = conectar()
        cur = conn.cursor()
        cur.execute("INSERT INTO nota (matricula, disciplina_id, valor) VALUES (?, ?, ?)",
                    (aluno_id, disc_id, float(entrada_nota.get())))
        conn.commit()
        conn.close()
        listar()
        limpar_campos()

    def alterar():
        if not validar_campos() or not id_nota.get().isdigit():
            return
        aluno_id, disc_id = obter_ids()
        conn = conectar()
        cur = conn.cursor()
        cur.execute("UPDATE nota SET matricula=?, disciplina_id=?, valor=? WHERE id=?",
                    (aluno_id, disc_id, float(entrada_nota.get()), int(id_nota.get())))
        conn.commit()
        conn.close()
        listar()
        limpar_campos()

    def excluir():
        if not id_nota.get().isdigit():
            return
        conn = conectar()
        cur = conn.cursor()
        cur.execute("DELETE FROM nota WHERE id=?", (int(id_nota.get()),))
        conn.commit()
        conn.close()
        listar()
        limpar_campos()

    def listar():
        conn = conectar()
        cur = conn.cursor()
        cur.execute("""SELECT nota.id, aluno.nome, disciplina.nome, nota.valor
                       FROM nota
                       JOIN aluno ON nota.matricula = aluno.matricula
                       JOIN disciplina ON nota.disciplina_id = disciplina.id""")
        dados = cur.fetchall()
        conn.close()
        exibir_resultado(dados)

    def filtrar():
        aluno_nome = filtro_aluno.get()
        disc_nome = filtro_disc.get()
        conn = conectar()
        cur = conn.cursor()
        query = """
            SELECT nota.id, aluno.nome, disciplina.nome, nota.valor
            FROM nota
            JOIN aluno ON nota.matricula = aluno.matricula
            JOIN disciplina ON nota.disciplina_id = disciplina.id
            WHERE 1=1
        """
        params = []
        if aluno_nome:
            query += " AND aluno.nome = ?"
            params.append(aluno_nome)
        if disc_nome:
            query += " AND disciplina.nome = ?"
            params.append(disc_nome)

        cur.execute(query, params)
        dados = cur.fetchall()
        conn.close()
        exibir_resultado(dados)

    def exibir_resultado(dados):
        texto.delete("1.0", tk.END)
        cab = f"{'ID':^5} | {'Aluno':^25} | {'Disciplina':^25} | {'Nota':^6}\n"
        texto.insert(tk.END, cab)
        texto.insert(tk.END, "-" * 70 + "\n")
        for id_, aluno, disc, nota in dados:
            linha = f"{id_:^5} | {aluno:^25} | {disc:^25} | {nota:^6.2f}\n"
            texto.insert(tk.END, linha)
        texto.insert(tk.END, "-" * 70 + "\n")

    # ==== Campos ====
    tk.Label(janela, text="ID", bg="#f0f8ff").grid(row=0, column=0, sticky="e", padx=5, pady=2)
    id_nota = tk.Entry(janela)
    id_nota.grid(row=0, column=1, sticky="we", padx=5, pady=2)

    tk.Label(janela, text="Aluno", bg="#f0f8ff").grid(row=1, column=0, sticky="e", padx=5, pady=2)
    cb_aluno = ttk.Combobox(janela, values=carregar_alunos(), state="readonly")
    cb_aluno.grid(row=1, column=1, sticky="we", padx=5, pady=2)

    tk.Label(janela, text="Disciplina", bg="#f0f8ff").grid(row=2, column=0, sticky="e", padx=5, pady=2)
    cb_disciplina = ttk.Combobox(janela, values=carregar_disciplinas(), state="readonly")
    cb_disciplina.grid(row=2, column=1, sticky="we", padx=5, pady=2)

    tk.Label(janela, text="Nota", bg="#f0f8ff").grid(row=3, column=0, sticky="e", padx=5, pady=2)
    entrada_nota = tk.Entry(janela)
    entrada_nota.grid(row=3, column=1, sticky="we", padx=5, pady=2)

    # ==== Botões ====
    frame_btn = tk.Frame(janela, bg="#f0f8ff")
    frame_btn.grid(row=4, column=0, columnspan=2, pady=10)

    btn_conf = {"width": 12, "padx": 5, "pady": 5, "font": ("Arial", 9, "bold"), "fg": "white"}
    tk.Button(frame_btn, text="Incluir", command=incluir, bg="#4caf50", **btn_conf).grid(row=0, column=0, padx=5)
    tk.Button(frame_btn, text="Alterar", command=alterar, bg="#2196f3", **btn_conf).grid(row=0, column=1, padx=5)
    tk.Button(frame_btn, text="Excluir", command=excluir, bg="#f44336", **btn_conf).grid(row=0, column=2, padx=5)
    tk.Button(frame_btn, text="Listar", command=listar, bg="#ff9800", **btn_conf).grid(row=0, column=3, padx=5)

    # ==== Filtro ====
    frame_filtro = tk.Frame(janela, bg="#dff0ff")
    frame_filtro.grid(row=5, column=0, columnspan=2, pady=5, sticky="ew")

    tk.Label(frame_filtro, text="Filtrar por Aluno:", bg="#dff0ff").grid(row=0, column=0, padx=5)
    filtro_aluno = ttk.Combobox(frame_filtro, values=[a.split(" - ")[1] for a in carregar_alunos()], state="readonly")
    filtro_aluno.grid(row=0, column=1, padx=5)

    tk.Label(frame_filtro, text="Disciplina:", bg="#dff0ff").grid(row=0, column=2, padx=5)
    filtro_disc = ttk.Combobox(frame_filtro, values=[d.split(" - ")[1] for d in carregar_disciplinas()], state="readonly")
    filtro_disc.grid(row=0, column=3, padx=5)

    tk.Button(frame_filtro, text="Aplicar Filtro", command=filtrar, bg="#6a5acd", fg="white", font=("Arial", 9, "bold")).grid(row=0, column=4, padx=10)

    # ==== Área de Texto ====
    texto = tk.Text(janela, height=10, width=70, bg="white", wrap="none", font=("Courier New", 10))
    texto.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

    scroll_x = tk.Scrollbar(janela, orient="horizontal", command=texto.xview)
    scroll_x.grid(row=7, column=0, columnspan=2, sticky="ew")
    texto.configure(xscrollcommand=scroll_x.set)

    janela.grid_columnconfigure(1, weight=1)
    janela.grid_rowconfigure(6, weight=1)

    listar()

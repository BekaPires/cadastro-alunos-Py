import sqlite3

def conectar():
    conn = sqlite3.connect("cadastro_de_alunos.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS aluno (
        matricula INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        data_nascimento TEXT NOT NULL
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS disciplina (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        turno TEXT NOT NULL,
        sala TEXT NOT NULL,
        professor TEXT NOT NULL
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS nota (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        valor REAL NOT NULL,
        matricula INTEGER,
        disciplina_id INTEGER,
        FOREIGN KEY(matricula) REFERENCES aluno(matricula) ON DELETE CASCADE,
        FOREIGN KEY(disciplina_id) REFERENCES disciplina(id) ON DELETE CASCADE
    )""")

    conn.commit()
    conn.close()

criar_tabelas()

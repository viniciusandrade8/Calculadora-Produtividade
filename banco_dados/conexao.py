
import sqlite3
from pathlib import Path


# Identifica a pasta principal do projeto.
PASTA_PROJETO = Path(__file__).resolve().parent.parent

# Define o local do arquivo do banco de dados.
PASTA_BANCO = PASTA_PROJETO / "dados"

ARQUIVO_BANCO = PASTA_BANCO / "producao.db"


def conectar():
    """Abre uma conexão com o banco SQLite."""
    PASTA_BANCO.mkdir(parents=True, exist_ok=True)

    conexao = sqlite3.connect(ARQUIVO_BANCO)
    conexao.execute("PRAGMA foreign_keys = ON")

    return conexao


def criar_tabelas():
    """Cria as tabelas iniciais do sistema."""

    with conectar() as conexao:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS maquinas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                custo_hora REAL NOT NULL DEFAULT 0,
                ativa INTEGER NOT NULL DEFAULT 1
            )
        """)

        conexao.execute("""
            CREATE TABLE IF NOT EXISTS moldes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                ciclo_segundos REAL NOT NULL,
                cavidades INTEGER NOT NULL,
                descricao TEXT
            )
        """)

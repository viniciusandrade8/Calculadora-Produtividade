
from banco_dados.conexao import conectar, criar_tabelas


criar_tabelas()

with conectar() as conexao:
    conexao.execute("""
        INSERT INTO maquinas (nome, custo_hora)
        VALUES (?, ?)
        ON CONFLICT(nome) DO UPDATE SET
            custo_hora = excluded.custo_hora
    """, ("Injetora de Teste", 150.00))

    maquinas = conexao.execute("""
        SELECT id, nome, custo_hora, ativa
        FROM maquinas
        ORDER BY id
    """).fetchall()

print("Máquinas cadastradas:")

for maquina in maquinas:
    print(maquina)

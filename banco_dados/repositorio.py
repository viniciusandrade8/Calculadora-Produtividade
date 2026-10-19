
from banco_dados.conexao import conectar


# -------------------------
# Validações
# -------------------------

def validar_nome(nome):
    if not nome or not nome.strip():
        raise ValueError("O nome não pode ficar vazio.")

    return nome.strip()


def validar_custo_hora(custo_hora):
    if custo_hora < 0:
        raise ValueError("O custo-hora não pode ser negativo.")


def validar_dados_molde(ciclo_segundos, cavidades):
    if ciclo_segundos <= 0:
        raise ValueError("O ciclo deve ser maior que zero.")

    if cavidades <= 0:
        raise ValueError("O número de cavidades deve ser maior que zero.")


# -------------------------
# Máquinas
# -------------------------

def cadastrar_maquina(nome, custo_hora):
    nome = validar_nome(nome)
    validar_custo_hora(custo_hora)

    with conectar() as conexao:
        cursor = conexao.execute(
            """
            INSERT INTO maquinas (nome, custo_hora)
            VALUES (?, ?)
            """,
            (nome, custo_hora),
        )

        return cursor.lastrowid


def listar_maquinas():
    with conectar() as conexao:
        return conexao.execute(
            """
            SELECT id, nome, custo_hora, ativa
            FROM maquinas
            ORDER BY nome
            """
        ).fetchall()


def atualizar_maquina(id_maquina, nome, custo_hora, ativa=True):
    nome = validar_nome(nome)
    validar_custo_hora(custo_hora)

    with conectar() as conexao:
        cursor = conexao.execute(
            """
            UPDATE maquinas
            SET nome = ?, custo_hora = ?, ativa = ?
            WHERE id = ?
            """,
            (nome, custo_hora, int(ativa), id_maquina),
        )

        if cursor.rowcount == 0:
            raise ValueError("Máquina não encontrada.")


# -------------------------
# Moldes
# -------------------------

def cadastrar_molde(
    nome, ciclo_segundos, cavidades, descricao=""
):
    nome = validar_nome(nome)
    validar_dados_molde(ciclo_segundos, cavidades)

    descricao = descricao.strip() if descricao else None

    with conectar() as conexao:
        cursor = conexao.execute(
            """
            INSERT INTO moldes (
                nome, ciclo_segundos, cavidades, descricao
            )
            VALUES (?, ?, ?, ?)
            """,
            (nome, ciclo_segundos, cavidades, descricao),
        )

        return cursor.lastrowid


def listar_moldes():
    with conectar() as conexao:
        return conexao.execute(
            """
            SELECT id, nome, ciclo_segundos, cavidades, descricao
            FROM moldes
            ORDER BY nome
            """
        ).fetchall()


def atualizar_molde(
    id_molde, nome, ciclo_segundos, cavidades, descricao=""
):
    nome = validar_nome(nome)
    validar_dados_molde(ciclo_segundos, cavidades)

    descricao = descricao.strip() if descricao else None

    with conectar() as conexao:
        cursor = conexao.execute(
            """
            UPDATE moldes
            SET nome = ?, ciclo_segundos = ?,
                cavidades = ?, descricao = ?
            WHERE id = ?
            """,
            (
                nome,
                ciclo_segundos,
                cavidades,
                descricao,
                id_molde,
            ),
        )

        if cursor.rowcount == 0:
            raise ValueError("Molde não encontrado.")

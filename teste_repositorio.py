
from banco_dados.conexao import criar_tabelas
from banco_dados.repositorio import (
    cadastrar_maquina,
    listar_maquinas,
    atualizar_maquina,
    cadastrar_molde,
    listar_moldes,
    atualizar_molde,
)


criar_tabelas()

# -------------------------
# Teste de máquina
# -------------------------

nome_maquina = "Injetora Aula 8"

maquinas = listar_maquinas()
maquina_existente = next(
    (m for m in maquinas if m[1] == nome_maquina),
    None,
)

if maquina_existente:
    id_maquina = maquina_existente[0]

    atualizar_maquina(
        id_maquina,
        nome_maquina,
        180.00,
        True,
    )
else:
    id_maquina = cadastrar_maquina(
        nome_maquina,
        180.00,
    )

print("\nMÁQUINAS CADASTRADAS")

for maquina in listar_maquinas():
    print(maquina)


# -------------------------
# Teste de molde
# -------------------------

nome_molde = "Molde Aula 8"

moldes = listar_moldes()
molde_existente = next(
    (m for m in moldes if m[1] == nome_molde),
    None,
)

if molde_existente:
    id_molde = molde_existente[0]

    atualizar_molde(
        id_molde,
        nome_molde,
        20.0,
        4,
        "Molde utilizado no teste da Aula 8",
    )
else:
    id_molde = cadastrar_molde(
        nome_molde,
        20.0,
        4,
        "Molde utilizado no teste da Aula 8",
    )

print("\nMOLDES CADASTRADOS")

for molde in listar_moldes():
    print(molde)


# -------------------------
# Teste de validação
# -------------------------

try:
    cadastrar_molde(
        "Molde Inválido",
        0,
        4,
        "Este cadastro deve falhar",
    )
except ValueError as erro:
    print("\nValidação funcionando:", erro)

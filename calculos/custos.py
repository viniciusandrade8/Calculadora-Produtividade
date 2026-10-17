
def validar_custo_hora(custo_hora):
    if custo_hora < 0:
        raise ValueError(
            "O custo-hora não pode ser negativo."
        )


def calcular_custo_por_dia(custo_hora, horas_por_dia):
    validar_custo_hora(custo_hora)

    if horas_por_dia <= 0:
        raise ValueError(
            "As horas por dia devem ser maiores que zero."
        )

    return custo_hora * horas_por_dia


def calcular_custo_por_mes(
    custo_hora, horas_por_dia, dias_por_mes
):
    validar_custo_hora(custo_hora)

    if horas_por_dia <= 0:
        raise ValueError(
            "As horas por dia devem ser maiores que zero."
        )

    if dias_por_mes <= 0:
        raise ValueError(
            "Os dias por mês devem ser maiores que zero."
        )

    return custo_hora * horas_por_dia * dias_por_mes


def calcular_custo_por_peca(custo_hora, pecas_por_hora):
    validar_custo_hora(custo_hora)

    if pecas_por_hora <= 0:
        raise ValueError(
            "A produção por hora deve ser maior que zero."
        )

    return custo_hora / pecas_por_hora

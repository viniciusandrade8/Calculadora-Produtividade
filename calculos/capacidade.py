
def validar_parametros(ciclo_segundos, cavidades):
    """Valida os parâmetros básicos de produção."""

    if ciclo_segundos <= 0:
        raise ValueError("O ciclo deve ser maior que zero.")

    if cavidades <= 0:
        raise ValueError("O número de cavidades deve ser maior que zero.")


def calcular_pecas_por_minuto(ciclo_segundos, cavidades):
    """Calcula a capacidade teórica de peças por minuto."""

    validar_parametros(ciclo_segundos, cavidades)

    return (60 / ciclo_segundos) * cavidades


def calcular_pecas_por_hora(ciclo_segundos, cavidades):
    """Calcula a capacidade teórica de peças por hora."""

    validar_parametros(ciclo_segundos, cavidades)

    return (3600 / ciclo_segundos) * cavidades


def calcular_producao_periodo(
    ciclo_segundos,
    cavidades,
    horas_por_dia,
    dias
):
    """Calcula a produção teórica de um período."""

    validar_parametros(ciclo_segundos, cavidades)

    if horas_por_dia <= 0:
        raise ValueError("As horas por dia devem ser maiores que zero.")

    if dias <= 0:
        raise ValueError("Os dias devem ser maiores que zero.")

    pecas_hora = calcular_pecas_por_hora(
        ciclo_segundos,
        cavidades
    )

    return pecas_hora * horas_por_dia * dias


def calcular_pecas_por_dia(
    ciclo_segundos,
    cavidades,
    horas_por_dia
):
    """Calcula a produção teórica diária."""

    return calcular_producao_periodo(
        ciclo_segundos,
        cavidades,
        horas_por_dia,
        1
    )


def calcular_pecas_por_mes(
    ciclo_segundos,
    cavidades,
    horas_por_dia,
    dias_por_mes
):
    """Calcula a produção teórica mensal."""

    return calcular_producao_periodo(
        ciclo_segundos,
        cavidades,
        horas_por_dia,
        dias_por_mes
    )

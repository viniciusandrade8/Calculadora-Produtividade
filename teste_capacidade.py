
from calculos.capacidade import (
    calcular_pecas_por_minuto,
    calcular_pecas_por_hora,
    calcular_pecas_por_dia,
    calcular_pecas_por_mes,
)


ciclo = 20
cavidades = 4
horas_por_dia = 8
dias_por_mes = 22

pecas_minuto = calcular_pecas_por_minuto(
    ciclo, cavidades
)

pecas_hora = calcular_pecas_por_hora(
    ciclo, cavidades
)

pecas_dia = calcular_pecas_por_dia(
    ciclo, cavidades, horas_por_dia
)

pecas_mes = calcular_pecas_por_mes(
    ciclo, cavidades, horas_por_dia, dias_por_mes
)

print(f"Peças por minuto: {pecas_minuto:.2f}")
print(f"Peças por hora: {pecas_hora:.2f}")
print(f"Peças por dia: {pecas_dia:.2f}")
print(f"Peças por mês: {pecas_mes:.2f}")

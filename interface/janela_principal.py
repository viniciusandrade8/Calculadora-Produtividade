
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QSlider,
    QSpinBox,
    QDoubleSpinBox,
    QGridLayout,
)
from PySide6.QtCore import Qt

from calculos.capacidade import (
    calcular_pecas_por_minuto,
    calcular_pecas_por_hora,
    calcular_pecas_por_dia,
    calcular_pecas_por_mes,
)

from calculos.custos import (
    calcular_custo_por_dia,
    calcular_custo_por_mes,
    calcular_custo_por_peca,
)

from interface.tela_cadastros import TelaCadastros


class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Sistema Industrial | Capacidade Produtiva"
        )
        self.resize(1200, 850)
        self.setMinimumSize(1000, 700)

        self.area_central = QWidget()
        self.setCentralWidget(self.area_central)

        self.layout_principal = QVBoxLayout(self.area_central)
        self.layout_principal.setContentsMargins(24, 24, 24, 24)
        self.layout_principal.setSpacing(20)

        self.criar_cabecalho()
        self.criar_area_conteudo()
        self.atualizar_resultados()

        self.menuBar().addAction(
            "Cadastros",
            self.abrir_cadastros
        )

    def criar_cabecalho(self):
        cabecalho = QFrame()
        cabecalho.setObjectName("cabecalho")

        layout = QVBoxLayout(cabecalho)
        layout.setContentsMargins(22, 18, 22, 18)
        layout.setSpacing(6)

        titulo = QLabel("Calculadora de Capacidade Produtiva")
        titulo.setObjectName("titulo")

        subtitulo = QLabel(
            "Simulação de produção e custos industriais"
        )
        subtitulo.setObjectName("subtitulo")

        layout.addWidget(titulo)
        layout.addWidget(subtitulo)

        self.layout_principal.addWidget(cabecalho)

    def criar_area_conteudo(self):
        layout_conteudo = QHBoxLayout()
        layout_conteudo.setSpacing(20)

        painel_parametros = self.criar_painel_parametros()
        painel_resultados = self.criar_painel_resultados()

        layout_conteudo.addWidget(painel_parametros, 2)
        layout_conteudo.addWidget(painel_resultados, 3)

        self.layout_principal.addLayout(layout_conteudo)
        self.layout_principal.setStretch(1, 1)

    def criar_controle(
        self, layout, rotulo, minimo, maximo, inicial, unidade
    ):
        texto = QLabel(rotulo)
        texto.setObjectName("rotulo_indicador")
        layout.addWidget(texto)

        linha = QHBoxLayout()
        linha.setSpacing(12)

        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(minimo, maximo)
        slider.setValue(inicial)
        slider.setMinimumWidth(100)

        campo = QSpinBox()
        campo.setRange(minimo, maximo)
        campo.setValue(inicial)
        campo.setSuffix(f" {unidade}")
        campo.setMinimumWidth(100)

        slider.valueChanged.connect(campo.setValue)
        campo.valueChanged.connect(slider.setValue)

        linha.addWidget(slider, 1)
        linha.addWidget(campo)

        layout.addLayout(linha)

        return campo

    def criar_campo_custo(self, layout):
        texto = QLabel("Custo-hora da máquina")
        texto.setObjectName("rotulo_indicador")
        layout.addWidget(texto)

        campo = QDoubleSpinBox()
        campo.setRange(0, 10000)
        campo.setDecimals(2)
        campo.setSingleStep(10)
        campo.setValue(150.00)
        campo.setPrefix("R$ ")
        campo.setMinimumWidth(150)

        layout.addWidget(campo)

        return campo

    def criar_painel_parametros(self):
        painel = QFrame()
        painel.setObjectName("painel")

        layout = QVBoxLayout(painel)
        layout.setContentsMargins(22, 22, 22, 22)
        layout.setSpacing(16)

        titulo = QLabel("Parâmetros de produção")
        titulo.setObjectName("titulo_painel")

        descricao = QLabel(
            "Configure o molde, o período e o custo da máquina."
        )
        descricao.setObjectName("descricao")
        descricao.setWordWrap(True)

        layout.addWidget(titulo)
        layout.addWidget(descricao)

        self.campo_ciclo = self.criar_controle(
            layout, "Tempo de ciclo", 5, 120, 20, "s"
        )

        self.campo_cavidades = self.criar_controle(
            layout, "Número de cavidades", 1, 32, 4, ""
        )

        self.campo_horas = self.criar_controle(
            layout, "Horas por dia", 1, 24, 8, "h"
        )

        self.campo_dias = self.criar_controle(
            layout, "Dias por mês", 1, 31, 22, "dias"
        )

        layout.addSpacing(8)

        self.campo_custo_hora = self.criar_campo_custo(layout)

        self.campo_ciclo.valueChanged.connect(
            self.atualizar_resultados
        )
        self.campo_cavidades.valueChanged.connect(
            self.atualizar_resultados
        )
        self.campo_horas.valueChanged.connect(
            self.atualizar_resultados
        )
        self.campo_dias.valueChanged.connect(
            self.atualizar_resultados
        )
        self.campo_custo_hora.valueChanged.connect(
            self.atualizar_resultados
        )

        layout.addStretch()

        return painel

    def criar_card_indicador(self, rotulo):
        card = QFrame()
        card.setObjectName("painel")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(8)

        titulo = QLabel(rotulo)
        titulo.setObjectName("rotulo_indicador")
        titulo.setWordWrap(True)

        valor = QLabel("0")
        valor.setObjectName("valor_indicador")
        valor.setWordWrap(True)

        layout.addWidget(titulo)
        layout.addWidget(valor)

        return card, valor

    def criar_painel_resultados(self):
        painel = QFrame()
        painel.setObjectName("painel")

        layout = QVBoxLayout(painel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        titulo = QLabel("Resultados da produção e custos")
        titulo.setObjectName("titulo_painel")

        descricao = QLabel(
            "Indicadores teóricos calculados com os parâmetros atuais."
        )
        descricao.setObjectName("descricao")
        descricao.setWordWrap(True)

        layout.addWidget(titulo)
        layout.addWidget(descricao)

        grade = QGridLayout()
        grade.setSpacing(12)

        card, self.valor_minuto = self.criar_card_indicador(
            "Peças por minuto"
        )
        grade.addWidget(card, 0, 0)

        card, self.valor_hora = self.criar_card_indicador(
            "Peças por hora"
        )
        grade.addWidget(card, 0, 1)

        card, self.valor_dia = self.criar_card_indicador(
            "Peças por dia"
        )
        grade.addWidget(card, 1, 0)

        card, self.valor_mes = self.criar_card_indicador(
            "Peças por mês"
        )
        grade.addWidget(card, 1, 1)

        card, self.valor_custo_dia = self.criar_card_indicador(
            "Custo de máquina por dia"
        )
        grade.addWidget(card, 2, 0)

        card, self.valor_custo_mes = self.criar_card_indicador(
            "Custo de máquina por mês"
        )
        grade.addWidget(card, 2, 1)

        card, self.valor_custo_peca = self.criar_card_indicador(
            "Custo de máquina por peça"
        )
        grade.addWidget(card, 3, 0, 1, 2)

        layout.addLayout(grade)

        observacao = QLabel(
            "Estimativa teórica: não inclui paradas, refugo, "
            "matéria-prima, mão de obra ou outros custos."
        )
        observacao.setObjectName("descricao")
        observacao.setWordWrap(True)

        layout.addWidget(observacao)
        layout.addStretch()

        return painel

    def formatar_quantidade(self, valor):
        return f"{valor:,.0f}".replace(",", ".")

    def formatar_moeda(self, valor, casas_decimais=2):
        valor_formatado = (
            f"{valor:,.{casas_decimais}f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )
        return f"R$ {valor_formatado}"

    def atualizar_resultados(self):
        ciclo = self.campo_ciclo.value()
        cavidades = self.campo_cavidades.value()
        horas = self.campo_horas.value()
        dias = self.campo_dias.value()
        custo_hora = self.campo_custo_hora.value()

        pecas_minuto = calcular_pecas_por_minuto(
            ciclo, cavidades
        )
        pecas_hora = calcular_pecas_por_hora(
            ciclo, cavidades
        )
        pecas_dia = calcular_pecas_por_dia(
            ciclo, cavidades, horas
        )
        pecas_mes = calcular_pecas_por_mes(
            ciclo, cavidades, horas, dias
        )

        custo_dia = calcular_custo_por_dia(
            custo_hora, horas
        )
        custo_mes = calcular_custo_por_mes(
            custo_hora, horas, dias
        )
        custo_peca = calcular_custo_por_peca(
            custo_hora, pecas_hora
        )

        self.valor_minuto.setText(
            self.formatar_quantidade(pecas_minuto)
        )
        self.valor_hora.setText(
            self.formatar_quantidade(pecas_hora)
        )
        self.valor_dia.setText(
            self.formatar_quantidade(pecas_dia)
        )
        self.valor_mes.setText(
            self.formatar_quantidade(pecas_mes)
        )

        self.valor_custo_dia.setText(
            self.formatar_moeda(custo_dia)
        )
        self.valor_custo_mes.setText(
            self.formatar_moeda(custo_mes)
        )
        self.valor_custo_peca.setText(
            self.formatar_moeda(custo_peca, 4)
        )
        
    def abrir_cadastros(self):
        tela = TelaCadastros(self)
        tela.exec()

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QTabWidget,
    QWidget,
    QLabel,
    QLineEdit,
    QDoubleSpinBox,
    QSpinBox,
    QTextEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView,
)

from banco_dados import repositorio


class TelaCadastros(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Cadastro de Máquinas e Moldes")
        self.resize(900, 600)

        layout_principal = QVBoxLayout(self)

        titulo = QLabel("Cadastros industriais")
        titulo.setObjectName("titulo")

        descricao = QLabel(
            "Gerencie as máquinas injetoras e os moldes "
            "utilizados nos cálculos de produção."
        )
        descricao.setObjectName("descricao")

        layout_principal.addWidget(titulo)
        layout_principal.addWidget(descricao)

        self.abas = QTabWidget()
        layout_principal.addWidget(self.abas)

        self.aba_maquinas = QWidget()
        self.aba_moldes = QWidget()

        self.abas.addTab(self.aba_maquinas, "Máquinas")
        self.abas.addTab(self.aba_moldes, "Moldes")

        self.montar_aba_maquinas()
        self.montar_aba_moldes()

        self.carregar_maquinas()
        self.carregar_moldes()

    # -------------------------
    # ABA DE MÁQUINAS
    # -------------------------

    def montar_aba_maquinas(self):
        layout = QVBoxLayout(self.aba_maquinas)

        formulario = QFormLayout()

        self.nome_maquina = QLineEdit()
        self.nome_maquina.setPlaceholderText(
            "Ex.: Injetora 150 toneladas"
        )

        self.custo_hora = QDoubleSpinBox()
        self.custo_hora.setRange(0, 1000000)
        self.custo_hora.setDecimals(2)
        self.custo_hora.setPrefix("R$ ")
        self.custo_hora.setValue(150.00)

        formulario.addRow("Nome da máquina:", self.nome_maquina)
        formulario.addRow("Custo por hora:", self.custo_hora)

        layout.addLayout(formulario)

        botoes = QHBoxLayout()

        botao_salvar = QPushButton("Salvar máquina")
        botao_novo = QPushButton("Novo / Limpar")
        botao_atualizar = QPushButton("Atualizar lista")

        botao_salvar.clicked.connect(self.salvar_maquina)
        botao_novo.clicked.connect(self.limpar_maquina)
        botao_atualizar.clicked.connect(self.carregar_maquinas)

        botoes.addWidget(botao_salvar)
        botoes.addWidget(botao_novo)
        botoes.addWidget(botao_atualizar)

        layout.addLayout(botoes)

        self.tabela_maquinas = QTableWidget(0, 4)
        self.tabela_maquinas.setHorizontalHeaderLabels(
            ["ID", "Máquina", "Custo/hora", "Ativa"]
        )
        self.configurar_tabela(self.tabela_maquinas)
        self.tabela_maquinas.cellClicked.connect(
            self.selecionar_maquina
        )

        layout.addWidget(self.tabela_maquinas)

    def carregar_maquinas(self):
        try:
            maquinas = repositorio.listar_maquinas()

            self.tabela_maquinas.setRowCount(0)

            for maquina in maquinas:
                id_maquina, nome, custo, ativa = maquina

                linha = self.tabela_maquinas.rowCount()
                self.tabela_maquinas.insertRow(linha)

                valores = [
                    str(id_maquina),
                    nome,
                    f"R$ {custo:,.2f}",
                    "Sim" if ativa else "Não",
                ]

                for coluna, valor in enumerate(valores):
                    self.tabela_maquinas.setItem(
                        linha,
                        coluna,
                        QTableWidgetItem(valor),
                    )

        except Exception as erro:
            QMessageBox.critical(
                self,
                "Erro",
                f"Não foi possível carregar as máquinas.\n{erro}",
            )

    def selecionar_maquina(self, linha, coluna):
        item_id = self.tabela_maquinas.item(linha, 0)

        if item_id is None:
            return

        nome = self.tabela_maquinas.item(linha, 1).text()
        custo_texto = self.tabela_maquinas.item(linha, 2).text()

        custo = float(
            custo_texto.replace("R$ ", "").replace(",", "")
        )

        self.id_maquina_selecionada = int(item_id.text())
        self.nome_maquina.setText(nome)
        self.custo_hora.setValue(custo)

    def salvar_maquina(self):
        nome = self.nome_maquina.text().strip()
        custo = self.custo_hora.value()

        try:
            id_selecionado = getattr(
                self, "id_maquina_selecionada", None
            )

            if id_selecionado is None:
                repositorio.cadastrar_maquina(nome, custo)
                mensagem = "Máquina cadastrada com sucesso."
            else:
                repositorio.atualizar_maquina(
                    id_selecionado, nome, custo
                )
                mensagem = "Máquina atualizada com sucesso."

            QMessageBox.information(self, "Sucesso", mensagem)
            self.limpar_maquina()
            self.carregar_maquinas()

        except Exception as erro:
            QMessageBox.warning(
                self,
                "Não foi possível salvar",
                str(erro),
            )

    def limpar_maquina(self):
        self.nome_maquina.clear()
        self.custo_hora.setValue(150.00)

        if hasattr(self, "id_maquina_selecionada"):
            del self.id_maquina_selecionada

        self.tabela_maquinas.clearSelection()

    # -------------------------
    # ABA DE MOLDES
    # -------------------------

    def montar_aba_moldes(self):
        layout = QVBoxLayout(self.aba_moldes)

        formulario = QFormLayout()

        self.nome_molde = QLineEdit()
        self.nome_molde.setPlaceholderText(
            "Ex.: Molde Tampa Superior"
        )

        self.ciclo_molde = QDoubleSpinBox()
        self.ciclo_molde.setRange(0.01, 100000)
        self.ciclo_molde.setDecimals(2)
        self.ciclo_molde.setSuffix(" s")
        self.ciclo_molde.setValue(20.00)

        self.cavidades_molde = QSpinBox()
        self.cavidades_molde.setRange(1, 1000)
        self.cavidades_molde.setValue(4)

        self.descricao_molde = QTextEdit()
        self.descricao_molde.setPlaceholderText(
            "Observações sobre o molde (opcional)"
        )
        self.descricao_molde.setMaximumHeight(65)

        formulario.addRow("Nome do molde:", self.nome_molde)
        formulario.addRow("Ciclo:", self.ciclo_molde)
        formulario.addRow("Cavidades:", self.cavidades_molde)
        formulario.addRow("Descrição:", self.descricao_molde)

        layout.addLayout(formulario)

        botoes = QHBoxLayout()

        botao_salvar = QPushButton("Salvar molde")
        botao_novo = QPushButton("Novo / Limpar")
        botao_atualizar = QPushButton("Atualizar lista")

        botao_salvar.clicked.connect(self.salvar_molde)
        botao_novo.clicked.connect(self.limpar_molde)
        botao_atualizar.clicked.connect(self.carregar_moldes)

        botoes.addWidget(botao_salvar)
        botoes.addWidget(botao_novo)
        botoes.addWidget(botao_atualizar)

        layout.addLayout(botoes)

        self.tabela_moldes = QTableWidget(0, 5)
        self.tabela_moldes.setHorizontalHeaderLabels(
            ["ID", "Molde", "Ciclo (s)", "Cavidades", "Descrição"]
        )
        self.configurar_tabela(self.tabela_moldes)
        self.tabela_moldes.cellClicked.connect(
            self.selecionar_molde
        )

        layout.addWidget(self.tabela_moldes)

    def carregar_moldes(self):
        try:
            moldes = repositorio.listar_moldes()

            self.tabela_moldes.setRowCount(0)

            for molde in moldes:
                id_molde, nome, ciclo, cavidades, descricao = molde

                linha = self.tabela_moldes.rowCount()
                self.tabela_moldes.insertRow(linha)

                valores = [
                    str(id_molde),
                    nome,
                    str(ciclo),
                    str(cavidades),
                    descricao or "",
                ]

                for coluna, valor in enumerate(valores):
                    self.tabela_moldes.setItem(
                        linha,
                        coluna,
                        QTableWidgetItem(valor),
                    )

        except Exception as erro:
            QMessageBox.critical(
                self,
                "Erro",
                f"Não foi possível carregar os moldes.\n{erro}",
            )

    def selecionar_molde(self, linha, coluna):
        item_id = self.tabela_moldes.item(linha, 0)

        if item_id is None:
            return

        self.id_molde_selecionado = int(item_id.text())
        self.nome_molde.setText(
            self.tabela_moldes.item(linha, 1).text()
        )
        self.ciclo_molde.setValue(
            float(self.tabela_moldes.item(linha, 2).text())
        )
        self.cavidades_molde.setValue(
            int(self.tabela_moldes.item(linha, 3).text())
        )
        self.descricao_molde.setPlainText(
            self.tabela_moldes.item(linha, 4).text()
        )

    def salvar_molde(self):
        nome = self.nome_molde.text().strip()
        ciclo = self.ciclo_molde.value()
        cavidades = self.cavidades_molde.value()
        descricao = self.descricao_molde.toPlainText()

        try:
            id_selecionado = getattr(
                self, "id_molde_selecionado", None
            )

            if id_selecionado is None:
                repositorio.cadastrar_molde(
                    nome, ciclo, cavidades, descricao
                )
                mensagem = "Molde cadastrado com sucesso."
            else:
                repositorio.atualizar_molde(
                    id_selecionado,
                    nome,
                    ciclo,
                    cavidades,
                    descricao,
                )
                mensagem = "Molde atualizado com sucesso."

            QMessageBox.information(self, "Sucesso", mensagem)
            self.limpar_molde()
            self.carregar_moldes()

        except Exception as erro:
            QMessageBox.warning(
                self,
                "Não foi possível salvar",
                str(erro),
            )

    def limpar_molde(self):
        self.nome_molde.clear()
        self.ciclo_molde.setValue(20.00)
        self.cavidades_molde.setValue(4)
        self.descricao_molde.clear()

        if hasattr(self, "id_molde_selecionado"):
            del self.id_molde_selecionado

        self.tabela_moldes.clearSelection()

    # -------------------------
    # CONFIGURAÇÃO COMPARTILHADA
    # -------------------------

    def configurar_tabela(self, tabela):
        tabela.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        tabela.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        tabela.setAlternatingRowColors(True)
        tabela.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        tabela.setColumnHidden(0, True)

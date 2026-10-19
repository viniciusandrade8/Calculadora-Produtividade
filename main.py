
import sys

from PySide6.QtWidgets import QApplication
from interface.janela_principal import JanelaPrincipal
from interface.estilo import obter_estilo

from banco_dados.conexao import criar_tabelas


def main():
    criar_tabelas()

    app = QApplication(sys.argv)

    app.setStyleSheet(obter_estilo())

    janela = JanelaPrincipal()

    # Preserve aqui a aplicação do tema, se já existir.
    janela.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

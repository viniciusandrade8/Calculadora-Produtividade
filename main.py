
import sys

from PySide6.QtWidgets import QApplication
from interface.janela_principal import JanelaPrincipal
from interface.estilo import obter_estilo


app = QApplication(sys.argv)

# Aplica o tema visual ao aplicativo
app.setStyleSheet(obter_estilo())

# Cria e exibe a janela principal
janela = JanelaPrincipal()
janela.show()

sys.exit(app.exec())

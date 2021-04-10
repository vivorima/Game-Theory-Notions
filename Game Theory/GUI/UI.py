import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import *
from Classes.game import *
from Classes.Joueur import Joueur
from Classes.Strat import Strat
from Classes.Profil import Profil


class Start(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal(int)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        # window Properties
        self.setWindowTitle('Stratégies Pures')
        self.setMinimumWidth(500)
        self.setMaximumWidth(500)
        self.setMinimumHeight(400)
        self.setMaximumHeight(400)

        # setting background color
        p = self.palette()
        from PyQt5.QtGui import QColor
        p.setColor(self.backgroundRole(), QColor(24, 24, 73))
        self.setPalette(p)

        # Layout Props
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)

        # Content
        self.desc = QtWidgets.QLabel(
            "Toutes les notions vues en stratégies pures dans un jeu à 2 joueurs et plus.")
        self.desc.setWordWrap(True)
        self.desc.setAlignment(QtCore.Qt.AlignCenter)

        self.button = QtWidgets.QPushButton('Créer un exemple')
        self.button.setAutoDefault(True)

        self.ex1 = QtWidgets.QPushButton('Exemple 2*3')
        self.ex2 = QtWidgets.QPushButton('Exemple 3*2')
        self.ex3 = QtWidgets.QPushButton('Exemple 3*3')
        self.ex4 = QtWidgets.QPushButton('Exemple à Somme nulle')

        # Adding Content to game_def
        layout.addWidget(self.desc)
        layout.addWidget(self.button)
        layout.addWidget(self.ex1)
        layout.addWidget(self.ex2)
        layout.addWidget(self.ex3)
        layout.addWidget(self.ex4)

        # Connecting
        self.button.clicked.connect(self.start)
        self.ex1.clicked.connect(self.exemple1)
        self.ex2.clicked.connect(self.exemple2)
        self.ex3.clicked.connect(self.exemple3)
        self.ex4.clicked.connect(self.exemple4)

        # Display
        self.setLayout(layout)

    def start(self):
        self.switch_window.emit(0)

    def exemple1(self):
        self.switch_window.emit(1)

    def exemple2(self):
        self.switch_window.emit(2)

    def exemple3(self):
        self.switch_window.emit(3)

    def exemple4(self):
        self.switch_window.emit(4)


class MainWindow(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal(str, str)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        # window Properties
        self.setWindowTitle('Strats Pures')
        self.setMinimumWidth(500)
        self.setMaximumWidth(500)
        self.setMinimumHeight(400)
        self.setMaximumHeight(400)

        # setting background color
        p = self.palette()
        from PyQt5.QtGui import QColor
        p.setColor(self.backgroundRole(), QColor(24, 24, 73))
        self.setPalette(p)

        # Layout Props
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(50, 80, 50, 80)

        # Content
        self.l1 = QLabel("Entrer les noms des joueurs:")
        self.l1.setWordWrap(True)
        self.l1.setAlignment(QtCore.Qt.AlignCenter)

        self.l2 = QLabel("Entrer les noms des strategies:")
        self.l2.setWordWrap(True)
        self.l2.setAlignment(QtCore.Qt.AlignCenter)

        self.nb = QLineEdit()
        self.nb.setPlaceholderText("Exemple:     J1,J2,J3")

        self.s = QLineEdit()
        self.s.setPlaceholderText("Exemple:     X,Y,Z/A,B/U,V")
        self.button = QPushButton('Confirmer')
        self.button.clicked.connect(self.switch)

        # adding the content
        layout.addWidget(self.l1)
        layout.addWidget(self.nb)
        layout.addWidget(self.l2)
        layout.addWidget(self.s)
        layout.addWidget(QLabel(""))
        layout.addWidget(self.button)

        self.setLayout(layout)

    def switch(self):
        if str(self.nb.text()) != "" and str(self.s.text()) != "":
            self.switch_window.emit(self.nb.text(), self.s.text())


class WindowTwo(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal(list, list)

    def __init__(self, nbj, s):
        QtWidgets.QWidget.__init__(self)
        # window Properties
        self.setWindowTitle('Strats Pures: Affectation de Gains.')
        self.setMinimumWidth(500)
        self.setMaximumWidth(500)
        self.setMinimumHeight(550)
        self.setMaximumHeight(550)

        # setting background color
        p = self.palette()
        from PyQt5.QtGui import QColor
        p.setColor(self.backgroundRole(), QColor(24, 24, 73))
        self.setPalette(p)

        # Layout Props
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(50, 30, 50, 30)

        # CREATION DES OBJETS JOUEURS
        Joueurs = nbj.split(",")
        for i in range(len(Joueurs)):
            nom = Joueurs[i]
            Joueurs[i] = Joueur(nom)

        # CREATION DES OBJETS STRATS
        strats = [l.split(',') for l in s.split('/') if l]

        for j in range(len(strats)):
            for s in range(len(strats[j])):
                nom = strats[j][s]
                strats[j][s] = Strat(nom, Joueurs[j])

        # AFFECTATION DES STRATS AUX JOUEURS
        for j in range(len(Joueurs)):
            Joueurs[j].ajouter_strats(strats[j])

        # ATTRIBUER DES GAINS AUX PROFILS
        self.Profils = get_Profils(Joueurs)
        self.Joueurs = Joueurs

        # Content
        playersText = QLabel('Joueurs:\n' + str(self.Joueurs)[1:-1])
        playersText.setWordWrap(True)
        playersText.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(playersText)
        layout.addWidget(QLabel('Entrer les gains de chaque profil:'))
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(len(self.Profils))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["Profils", "Gains"])

        # afficher les profils
        for i in range(len(self.Profils)):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(self.Profils[i].__repr__()))

        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.button = QPushButton('Confirmer')
        self.button.clicked.connect(self.switch)

        # Adding to the layout
        layout.addWidget(self.tableWidget)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def switch(self):
        # verifie si il existe des gains ou pas
        Gains = []
        problem = False
        for g in range(len(self.Profils)):
            item = self.tableWidget.item(g, 1)
            if item is not None and str(item.text()) != "":
                text = item.text()
                test_list = text.split(",")
                for i in range(0, len(test_list)):
                    test_list[i] = int(test_list[i])
                Gains.append(test_list)
            else:
                print("Empty Field")
                problem = True
        if not problem:
            Ajouter_Gains(self.Profils, Gains)
            Attribuer_Profils(self.Joueurs, self.Profils)
            self.switch_window.emit(self.Joueurs, self.Profils)


class BOARD(QtWidgets.QWidget):

    def __init__(self, J, P):
        self.players = J
        self.profils = P
        QtWidgets.QWidget.__init__(self)
        # window Properties
        self.setWindowTitle('Stratégies Pures: Resultats.')
        self.setMinimumWidth(900)
        self.setMaximumWidth(1500)
        self.setMinimumHeight(700)
        self.setMaximumHeight(1200)

        # setting background color
        p = self.palette()
        from PyQt5.QtGui import QColor
        p.setColor(self.backgroundRole(), QColor(24, 24, 73))
        self.setPalette(p)

        # Layout Props setContentsMargins(50, 30, 50, 30)
        self.bigL = QVBoxLayout()
        self.layout = QHBoxLayout()
        self.subl = QHBoxLayout()
        self.subr = QVBoxLayout()

        # Content
        self.label = QtWidgets.QLabel('Clickez sur un bouton à droite pour afficher les resultats:')
        self.label.setWordWrap(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.output = QTextBrowser()
        self.data = QTextBrowser()
        self.data.setFixedWidth(240)
        self.StratStrict = QPushButton('Strats strictement\n dominantes')
        self.StratFaible = QPushButton('Strats faiblement\n dominantes')
        self.nash = QPushButton('Equilibre de Nash')
        self.pareto = QPushButton('Optimum de Pareto')
        self.niv = QPushButton('Niveaux de Securité')
        self.valeur = QPushButton('Somme Nulle')

        self.data.setText('<span style=\" color: rgb(247, 58, 77);\">%s</span>' % "Vos Données:")
        self.data.append('\n'.join(map(str, self.players)))
        self.data.append('<span style=\" color: rgb(247, 58, 77);\">%s</span>' % "Profils:")
        self.data.append('\n'.join(map(str, self.profils)))

        # Adding the content
        self.subl.addWidget(self.data)
        self.subl.addWidget(self.output)

        self.subr.addWidget(self.StratStrict)
        self.subr.addWidget(self.StratFaible)
        self.subr.addWidget(self.nash)
        self.subr.addWidget(self.pareto)
        self.subr.addWidget(self.niv)
        self.subr.addWidget(self.valeur)

        self.layout.addLayout(self.subl)
        self.layout.addLayout(self.subr)

        self.bigL.addWidget(self.label)
        self.bigL.addLayout(self.layout)

        self.StratStrict.clicked.connect(self.print_strict)
        self.StratFaible.clicked.connect(self.print_faibl)
        self.nash.clicked.connect(self.print_nash)
        self.pareto.clicked.connect(self.print_pareto)
        self.niv.clicked.connect(self.print_Nivs)
        self.valeur.clicked.connect(self.print_valeur)

        self.setLayout(self.bigL)

    @pyqtSlot()
    def print_strict(self):
        self.output.setText(
            '<span style=\" color: rgb(247, 58, 77);\">%s</span>' % "Stratégies Strictement dominanates")

        self.output.append(strats_strict_dominantes(self.players))

    @pyqtSlot()
    def print_faibl(self):
        self.output.setText(
            '<span style=\" color: rgb(247, 58, 77);\">%s</span>' % "Stratégies Faiblement dominanates")
        self.output.append(strats_faible_dominantes(self.players))

    @pyqtSlot()
    def print_nash(self):
        self.output.setText(
            '<span style=\" color: rgb(247, 58, 77);\">%s</span>' % "Equilibre de Nash")
        self.output.append(Nash(self.players))

    @pyqtSlot()
    def print_pareto(self):
        self.output.setText(
            '<span style=\" color: rgb(247, 58, 77);\">%s</span>' % "Optimum de Pareto")
        self.output.append(str(Optimum_Pareto(self.profils)))

    @pyqtSlot()
    def print_Nivs(self):
        self.output.setText(
            '<span style=\" color: rgb(247, 58, 77);\">%s</span>' % "Niveaux de Securite")
        self.output.append(affiche_Nivs(self.players))

    @pyqtSlot()
    def print_valeur(self):
        self.output.setText(
            '<span style=\" color: rgb(247, 58, 77);\">%s</span>' % "Somme Nulle")
        self.output.append(SommeNulle(self.players, self.profils))


class Controller:

    def __init__(self):
        pass

    def show_login(self):
        self.login = Start()
        self.login.switch_window.connect(self.show_main)
        self.login.show()

    def show_main(self, nb):
        if nb == 0:
            self.window = MainWindow()
            self.window.switch_window.connect(self.show_window_two)
            self.login.close()
            self.window.show()
        else:
            Joueurs = []
            Profils = []
            if nb == 4:
                Joueurs = [j("J1"), j("J2")]

                Joueurs[0].ajouter_strats([s("X", Joueurs[0]), s("Y", Joueurs[0]), s("Z", Joueurs[0])])
                Joueurs[1].ajouter_strats([s("T", Joueurs[1]), s("U", Joueurs[1]), s("V", Joueurs[1])])

                Profils = get_Profils(Joueurs)
                Gains = [
                    [3, -3],
                    [4, -4],
                    [5, -5],
                    [-1, 1],
                    [7, -7],
                    [2, -2],
                    [2, -2],
                    [-5, 5],
                    [3, -3]
                ]
                Ajouter_Gains(Profils, Gains)
                Attribuer_Profils(Joueurs, Profils)
            if nb == 1:
                Joueurs = [j("J1"), j("J2")]

                Joueurs[0].ajouter_strats([s("X", Joueurs[0]), s("Y", Joueurs[0]), s("Z", Joueurs[0])])
                Joueurs[1].ajouter_strats([s("T", Joueurs[1]), s("U", Joueurs[1]), s("V", Joueurs[1])])

                Profils = get_Profils(Joueurs)
                Gains = [
                    [3, 2],
                    [4, 0],
                    [5, 1],
                    [1, 0],
                    [7, 3],
                    [2, 5],
                    [2, 0],
                    [8, 5],
                    [1, 7]
                ]
                Ajouter_Gains(Profils, Gains)
                Attribuer_Profils(Joueurs, Profils)
            if nb == 2:
                Joueurs = [j("J1"), j("J2"), j("J3")]

                Joueurs[0].ajouter_strats([s("X", Joueurs[0]), s("Y", Joueurs[0]), s("Z", Joueurs[0])])
                Joueurs[1].ajouter_strats([s("T", Joueurs[1]), s("U", Joueurs[1]), s("V", Joueurs[1])])
                Joueurs[2].ajouter_strats([s("A", Joueurs[2]), s("B", Joueurs[2])])

                Profils = get_Profils(Joueurs)
                Gains = [
                    [3, 2, 1],  # (X, T, A)
                    [4, 0, 3],  # (X, T, B)
                    [5, 1, 2],  # (X, U, A)
                    [1, 0, 0],  # (X, U, B)
                    [7, 3, 2],  # (X, V, A)
                    [2, 5, 0],  # (X, V, B)
                    [2, 0, -1],  # (Y, T, A)
                    [8, 5, 2],  # (Y, T, B)
                    [1, 7, 8],  # (Y, U, A)
                    [0, 2, 3],  # (Y, U, B)
                    [2, 0, 1],  # (Y, V, A)
                    [3, 1, -1],  # (Y, V, B)
                    [1, 2, 0],  # (Z, T, A),
                    [2, 3, 4],  # (Z, T, B),
                    [1, 4, 2],  # (Z, U, A),
                    [3, 1, 2],  # (Z, U, B),
                    [0, 0, 2],  # (Z, V, A),
                    [1, 3, 4]  # (Z, V, B)
                ]
                Ajouter_Gains(Profils, Gains)
                Attribuer_Profils(Joueurs, Profils)
            if nb == 3:
                Joueurs = [j("Leo"), j("Raj"), j("Sheldon")]

                Joueurs[0].ajouter_strats([s("Movies", Joueurs[0]), s("Home", Joueurs[0])])
                Joueurs[1].ajouter_strats([s("Movies", Joueurs[1]), s("Home", Joueurs[1])])
                Joueurs[2].ajouter_strats([s("Movies", Joueurs[2]), s("Home", Joueurs[2])])

                Profils = get_Profils(Joueurs)
                Gains = [
                    [-4, -4, -4],
                    [4, 4, 1],
                    [-4, 1, 4],
                    [-1, 1, 1],
                    [1, -4, 4],
                    [1, -1, 1],
                    [1, 1, -4],
                    [1, 1, 1],

                ]
                Ajouter_Gains(Profils, Gains)
                Attribuer_Profils(Joueurs, Profils)

            if Joueurs is not None and Profils is not None:
                self.board = BOARD(Joueurs, Profils)
                self.login.close()
                self.board.show()
            else:
                print("Probleme à la ligne 420")

    def show_window_two(self, nbj, s):
        self.window_two = WindowTwo(nbj, s)
        self.window_two.switch_window.connect(self.show_board)
        self.window.close()
        self.window_two.show()

    def show_board(self, J, P):
        self.board = BOARD(J, P)
        self.window_two.close()
        self.board.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(open('StyleSheet.css').read())
    controller = Controller()
    controller.show_login()
    sys.exit(app.exec_())

import sys
from fractions import Fraction

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import *

from Algos import get_Profils, Ajouter_Gains, Attribuer_Profils, isfloat, isNash, isfraction, trouver_Nash, isaccepted
from Joueur import Joueur
from Strat import Strat


class DataWindow(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal(int, str, str)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        # window Properties
        self.setWindowTitle('Strats Mixtes: Données')
        self.setMinimumWidth(500)
        self.setMaximumWidth(500)
        self.setMinimumHeight(500)
        self.setMaximumHeight(700)

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
            "Calculer l’équilibre de Nash mixte dans un jeu à deux joueurs avec au maximum 3 stratégies chacun")
        self.desc.setWordWrap(True)
        self.desc.setAlignment(QtCore.Qt.AlignCenter)

        self.l1 = QLabel("Entrer les noms des joueurs:")
        self.l1.setWordWrap(True)
        self.l1.setAlignment(QtCore.Qt.AlignCenter)

        self.l2 = QLabel("Entrer les noms des strategies: ")
        self.l2.setWordWrap(True)
        self.l2.setAlignment(QtCore.Qt.AlignCenter)

        self.nb = QLineEdit()
        self.nb.setPlaceholderText("Exemple:     J1,J2")

        self.s = QLineEdit()
        self.s.setPlaceholderText("Exemple:     X,Y,Z/A,B,C")
        self.button = QPushButton('Ok')
        self.button.clicked.connect(self.switch)
        self.exp1 = QPushButton('Exemple 1')
        self.exp1.clicked.connect(self.switchexp1)
        self.exp2 = QPushButton('Exemple 2')
        self.exp2.clicked.connect(self.switchexp2)
        self.exp3 = QPushButton('Exemple 3')
        self.exp3.clicked.connect(self.switchexp3)

        # adding the content
        layout.addWidget(self.desc)
        layout.addWidget(QLabel(""))
        layout.addWidget(self.l1)
        layout.addWidget(self.nb)
        layout.addWidget(self.l2)
        layout.addWidget(self.s)
        layout.addWidget(QLabel(""))
        layout.addWidget(self.button)
        layout.addWidget(self.exp1)
        layout.addWidget(self.exp2)
        layout.addWidget(self.exp3)

        self.setLayout(layout)

    def switch(self):
        if str(self.nb.text()) != "" and str(self.s.text()) != "":
            self.switch_window.emit(0, self.nb.text(), self.s.text())

    def switchexp1(self):
        self.switch_window.emit(1, "", "")

    def switchexp2(self):
        self.switch_window.emit(2, "", "")

    def switchexp3(self):
        self.switch_window.emit(3, "", "")


class GainsWindow(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal(list, list)

    def __init__(self, nbj, s):
        QtWidgets.QWidget.__init__(self)
        # window Properties
        self.setWindowTitle('Strats Mixtes: Gains.')
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


class Board(QtWidgets.QWidget):

    def __init__(self, J, P):
        self.players = J
        self.profils = P
        QtWidgets.QWidget.__init__(self)
        # window Properties
        self.setWindowTitle('Strats Mixtes: Nash.')
        self.setMinimumWidth(1000)
        self.setMaximumWidth(1000)
        self.setMinimumHeight(500)
        self.setMaximumHeight(500)

        # setting background color
        p = self.palette()
        from PyQt5.QtGui import QColor
        p.setColor(self.backgroundRole(), QColor(24, 24, 73))
        self.setPalette(p)

        # layouts
        self.bigL = QVBoxLayout()
        self.layout = QHBoxLayout()
        self.lr = QHBoxLayout()
        self.ll = QVBoxLayout()

        # content
        self.label = QtWidgets.QLabel('Entrer des Stratégies mixtes :')
        self.label.setWordWrap(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.mixte1 = QLineEdit()
        self.mixte1.setPlaceholderText("        Joueur1 = (1/4, 1/2, 1/4)")
        self.mixte2 = QLineEdit()
        self.mixte2.setPlaceholderText("        Joueur2 = (0, 1, 0)")
        self.output = QTextBrowser()
        self.data = QTextBrowser()
        self.data.setFixedWidth(200)
        self.data.setText('<span style=\" color: rgb(247, 58, 77);\">%s</span>' % "Vos Données:")
        self.data.append('\n'.join(map(str, self.players)))
        self.data.append('<span style=\" color: rgb(247, 58, 77);\">%s</span>' % "Profils:")
        self.data.append('\n'.join(map(str, self.profils)))
        self.isNash = QPushButton("is Nash?")
        self.Find = QPushButton("Find Nash")
        self.isNash.clicked.connect(self.print_isnash)
        self.Find.clicked.connect(self.print_FindNash)

        self.ll.addWidget(self.Find)
        self.ll.addWidget(self.data)
        self.lr.addLayout(self.ll)
        self.lr.addWidget(self.output)
        self.layout.addWidget(self.mixte1)
        self.layout.addWidget(self.mixte2)
        self.layout.addWidget(self.isNash)
        self.bigL.addWidget(self.label)

        self.bigL.addLayout(self.layout)
        self.bigL.addLayout(self.lr)
        self.setLayout(self.bigL)

    @pyqtSlot()
    def print_isnash(self):
        self.output.setText(
            '<span style=\" color: rgb(247, 58, 77);\">%s</span>' % "Ce profil est-il un équilibre de Nash? \n Méthode: Invariance au Support\n")
        temp = [ele if isaccepted(ele) else "" for ele in self.mixte1.text().split(",")]
        temp2 = [ele if isaccepted(ele) else "" for ele in self.mixte2.text().split(",")]

        print(self.mixte1.text(), self.mixte2.text(), temp, temp2, self.players)
        # i dont want to accept 0.2 --> enter just the fractions
        if len(temp) == len(self.players[0].strats) and len(temp2) == len(self.players[1].strats):
            if all(isaccepted(x) for x in temp) and all(isaccepted(x) for x in temp2):
                # convert to fractions from string
                temp = [Fraction(ele) for ele in temp]
                temp2 = [Fraction(ele) for ele in temp2]
                print(self.mixte1.text(), self.mixte2.text(), temp, temp2)
                if sum(temp) == 1 and sum(temp2) == 1:
                    self.players[0].ajouter_mixte(temp)
                    self.players[1].ajouter_mixte(temp2)
                    b, s = isNash(self.players)
                    self.output.append(s)
                else:
                    self.output.append("La somme != 1")
            else:
                self.output.append("Que les fractions et 0<=chiffres<=1 sont acceptés")
        else:
            # self.output.append("Vous avez entrer des probas pour (" + str(len(temp)) + "," + str(len(temp2)) + ") \
            # stratégies au lieu de (" + str(len(self.players[0].strats)) + "," + str(len(self.players[1].strats)) + ")")
            self.output.append("Vérifier le format des probabilités, format attendu:" + "(" + str(
                len(self.players[0].strats)) + "," + str(
                len(self.players[1].strats)) + ")" + "\nFormat donné: " + "(" + str(len(temp)) + "," + str(
                len(temp2)) + ")")

    @pyqtSlot()
    def print_FindNash(self):
        self.output.setText(
            '<span style=\" color: rgb(247, 58, 77);\">%s</span>' % "Trouver un équilibre de Nash")
        self.output.append(trouver_Nash(self.players, self.profils))


class Controller:

    def __init__(self):
        pass

    def show_data_window(self):
        self.data_window = DataWindow()
        self.data_window.switch_window.connect(self.show_gain_window)
        self.data_window.show()

    def show_gain_window(self, num, nbj, s):
        if num == 0:
            self.gains_window = GainsWindow(nbj, s)
            self.gains_window.switch_window.connect(self.show_board)
            self.data_window.close()
            self.gains_window.show()
        elif num == 1:
            Joueurs = [Joueur("J1"), Joueur("J2")]
            Joueurs[0].ajouter_strats([Strat("X", Joueurs[0]), Strat("Y", Joueurs[0]), Strat("Z", Joueurs[0])])
            Joueurs[1].ajouter_strats([Strat("A", Joueurs[1]), Strat("B", Joueurs[1]), Strat("C", Joueurs[1])])
            Profils = get_Profils(Joueurs)
            Gains = [
                [0, 0],
                [-1, 1],
                [1, -1],
                [1, -1],
                [0, 0],
                [-1, 1],
                [-1, 1],
                [1, -1],
                [0, 0]
            ]
            Ajouter_Gains(Profils, Gains)
            Attribuer_Profils(Joueurs, Profils)
            self.board = Board(Joueurs, Profils)
            self.data_window.close()
            self.board.show()
        elif num == 2:
            Joueurs = [Joueur("J1"), Joueur("J2")]
            Joueurs[0].ajouter_strats([Strat("X", Joueurs[0]), Strat("Y", Joueurs[0])])
            Joueurs[1].ajouter_strats([Strat("A", Joueurs[1]), Strat("B", Joueurs[1]), Strat("C", Joueurs[1])])
            Profils = get_Profils(Joueurs)
            Gains = [
                [1, 0.5],
                [1, -1],
                [-1, -0.5],
                [2, -1],
                [-1, 3],
                [0, 2]
            ]
            Ajouter_Gains(Profils, Gains)
            Attribuer_Profils(Joueurs, Profils)
            self.board = Board(Joueurs, Profils)
            self.data_window.close()
            self.board.show()
        elif num == 3:

            Joueurs = [Joueur("J1"), Joueur("J2")]
            Joueurs[0].ajouter_strats([Strat("X", Joueurs[0]), Strat("Y", Joueurs[0]), Strat("Z", Joueurs[0])])
            Joueurs[1].ajouter_strats([Strat("A", Joueurs[1]), Strat("B", Joueurs[1])])
            Profils = get_Profils(Joueurs)
            Gains = [
                [3, 3],
                [3, 2],
                [2, 2],
                [5, 6],
                [0, 3],
                [6, 1]
            ]

            Ajouter_Gains(Profils, Gains)
            Attribuer_Profils(Joueurs, Profils)
            self.board = Board(Joueurs, Profils)
            self.data_window.close()
            self.board.show()

    def show_board(self, J, P):
        self.board = Board(J, P)
        self.gains_window.close()
        self.board.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(open('StyleSheet.css').read())
    controller = Controller()
    controller.show_data_window()
    sys.exit(app.exec_())

# self.ex1 = QtWidgets.QPushButton('Vérifier si un profil donné \n est un equilibre de Nash')
# self.ex2 = QtWidgets.QPushButton('Trouver un equilibre de Nash')

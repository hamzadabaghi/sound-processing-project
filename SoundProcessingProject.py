# Sound Processing Project , Hamza Dabaghi
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import Program as Program

# generated with Qt designer


class Ui_MainWindow(object):

    # first sound path

    firstPath = ""

    # second sound path

    secondPath = ""

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setAutoFillBackground(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.ImageResultLabel = QtWidgets.QLabel(self.centralwidget)
        self.ImageResultLabel.setGeometry(QtCore.QRect(300, 20, 461, 391))
        self.ImageResultLabel.setText("")
        self.ImageResultLabel.setObjectName("ImageResultLabel")
        self.DistanceLabel = QtWidgets.QLabel(self.centralwidget)
        self.DistanceLabel.setGeometry(QtCore.QRect(340, 480, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.DistanceLabel.setFont(font)
        self.DistanceLabel.setObjectName("DistanceLabel")
        self.DistanceResultLabel = QtWidgets.QLabel(self.centralwidget)
        self.DistanceResultLabel.setGeometry(QtCore.QRect(510, 480, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.DistanceResultLabel.setFont(font)
        self.DistanceResultLabel.setObjectName("DistanceResultLabel")
        self.ImportFirstSoundButton = QtWidgets.QPushButton(self.centralwidget)
        self.ImportFirstSoundButton.setGeometry(QtCore.QRect(90, 110, 151, 51))
        self.ImportFirstSoundButton.setObjectName("ImportFirstSoundButton")
        self.FirstSoundLabel = QtWidgets.QLabel(self.centralwidget)
        self.FirstSoundLabel.setGeometry(QtCore.QRect(70, 170, 181, 21))
        self.FirstSoundLabel.setAutoFillBackground(True)
        self.FirstSoundLabel.setStyleSheet("color: rgb(255, 0, 0);")
        self.FirstSoundLabel.setText("")
        self.FirstSoundLabel.setObjectName("FirstSoundLabel")
        self.ImportSecondSoundButton = QtWidgets.QPushButton(
            self.centralwidget)
        self.ImportSecondSoundButton.setGeometry(
            QtCore.QRect(90, 240, 151, 51))
        self.ImportSecondSoundButton.setObjectName("ImportSecondSoundButton")
        self.SecondSoundLabel = QtWidgets.QLabel(self.centralwidget)
        self.SecondSoundLabel.setGeometry(QtCore.QRect(70, 300, 181, 21))
        self.SecondSoundLabel.setAutoFillBackground(True)
        self.SecondSoundLabel.setStyleSheet("color: rgb(255, 0, 0);")
        self.SecondSoundLabel.setText("")
        self.SecondSoundLabel.setObjectName("SecondSoundLabel")
        self.calculateDistanceButton = QtWidgets.QPushButton(
            self.centralwidget)
        self.calculateDistanceButton.setGeometry(
            QtCore.QRect(110, 382, 111, 41))
        self.calculateDistanceButton.setObjectName("calculateDistanceButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.dialog = QtWidgets.QFileDialog(self.centralwidget)
        self.dialog.setWindowTitle('Ouvrir fichier .wav')
        self.dialog.setNameFilter('(*.wav)')

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.DistanceLabel.setText(_translate("MainWindow", "La distance  : "))
        self.DistanceResultLabel.setText(_translate("MainWindow", "0"))
        self.ImportFirstSoundButton.setText(
            _translate("MainWindow", "Import the first sound "))
        self.ImportSecondSoundButton.setText(
            _translate("MainWindow", "Import the second sound "))
        self.calculateDistanceButton.setText(
            _translate("MainWindow", "Calculate distance"))

    # connect our buttons
        self.ImportFirstSoundButton.clicked.connect(self.importFile1)
        self.ImportSecondSoundButton.clicked.connect(self.importFile2)
        self.calculateDistanceButton.clicked.connect(self.compare)

    # Function File 1

    def importFile1(self):
        self.dialog.setDirectory(QtCore.QDir.currentPath())
        self.dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        if self.dialog.exec_() == QtWidgets.QDialog.Accepted:
            file_full_path = str(self.dialog.selectedFiles()[0])
        else:
            return None
        self.FirstSoundLabel.setText(file_full_path)
        self.firstPath = file_full_path

    # Function File 2

    def importFile2(self):
        self.dialog.setDirectory(QtCore.QDir.currentPath())
        self.dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        if self.dialog.exec_() == QtWidgets.QDialog.Accepted:
            file_full_path = str(self.dialog.selectedFiles()[0])
        else:
            return None
        self.SecondSoundLabel.setText(file_full_path)
        self.secondPath = file_full_path

    # Function compare

    def compare(self):
        # Tester si l'un des chemin est vide
        if self.firstPath == "":
            self.FirstSoundLabel.setText(
                "nothing is imported yet")
        if self.secondPath == "":
            self.SecondSoundLabel.setText(
                "nothing is imported yet")

        # import audio files with librosa library

        """
            Les coefficients cepstraux de fréquence mel (MFCC) d'un signal
            sont un petit ensemble de caractéristiques (généralement environ 10-20)
            qui décrivent de manière concise la forme globale d'une enveloppe spectrale.
        
        """
        x1, sr1 = librosa.load(self.firstPath)
        x2, sr2 = librosa.load(self.secondPath)

        # mfcc parametrization to get features from our audio files ( feature vectors )

        """
            librosa.feature.mfcc calcule les MFCC sur un signal audio

        """
        C1_cens = librosa.feature.mfcc(x1, sr=sr1)
        C2_cens = librosa.feature.mfcc(x2, sr=sr2)

        doComparaison = Program.Program()

        """ Etape 1 : Construction de la table des coûts

            Nous créons un tableau où la cellule (i, j)
            stocke le coût optimal de dtw (x [: i], y [: j]),
            c'est-à-dire le coût optimal de (0, 0) à (i, j).
            Tout d'abord, nous résolvons les cas aux limites,
            c'est-à-dire lorsque l'une des deux séquences est vide.
            Ensuite, nous remplissons le tableau du haut à gauche
            vers le bas à droite.
        """

        D = doComparaison.dtw_table(C1_cens.T, C2_cens.T)
        totalDistance = D[-1, -1]

        self.DistanceResultLabel.setText(str(totalDistance))

        """ Etape 2 : Retour en arrière

            Pour assembler le meilleur chemin,
            nous utilisons le retour en arrière
            Nous allons commencer à la fin, (Nx − 1, Ny − 1), et revenir au début

        """

        dtw = doComparaison.dtw(C1_cens.T, C2_cens.T, D)

        """ Évaluer : Visualisation des deux signaux et leur alignements 
        
        
        Si les deux formes d'onde étaient identiques, 
        leurs échantillons seraient joués aux mêmes instances 
        et la matrice de coût décrirait une ligne droite 
        ce qui signifie que l'échantillon 0 sur x se trouve sur l'échantillon 0 sur y
        ,l'échantillon 1 sur x se trouve sur 1 dans y
         et ainsi de suite jusqu'à l'échantillon N.
         
         """
        wp_s = np.asarray(dtw)

        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111)
        librosa.display.specshow(D, x_axis='time', y_axis='time',
                                 cmap='gray_r')
        imax = ax.imshow(D, cmap=plt.get_cmap('gray_r'),
                         origin='lower', interpolation='nearest', aspect='auto')
        ax.plot(wp_s[:, 1], wp_s[:, 0], marker='o', color='r')
        plt.title('Warping Path ')
        plt.colorbar()
        plt.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

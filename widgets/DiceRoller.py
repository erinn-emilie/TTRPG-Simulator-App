import random

from PyQt6 import QtCore
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class DiceRoller(QMainWindow):
    def __init__(self):
        super().__init__()

        #################### FIRST INTERFACE START ####################

        # all standard dice
        self.d4 = QPushButton("d4")
        self.d4.setFixedSize(88, 88)
        self.d4.setIcon(QIcon("assets/d4.png"))
        self.d4.clicked.connect(self.d4clicked)
        self.d6 = QPushButton("d6")
        self.d6.setFixedSize(88, 88)
        self.d6.setIcon(QIcon("assets/d6.png"))
        self.d6.clicked.connect(self.d6clicked)
        self.d8 = QPushButton("d8")
        self.d8.setFixedSize(88, 88)
        self.d8.setIcon(QIcon("assets/d8.png"))
        self.d8.clicked.connect(self.d8clicked)
        self.d10 = QPushButton("d10")
        self.d10.setFixedSize(88, 88)
        self.d10.setIcon(QIcon("assets/d10.png"))
        self.d10.clicked.connect(self.d10clicked)
        self.d12 = QPushButton("d12")
        self.d12.setFixedSize(88, 88)
        self.d12.setIcon(QIcon("assets/d12.png"))
        self.d12.clicked.connect(self.d12clicked)
        self.d20 = QPushButton("d20")
        self.d20.setFixedSize(88, 88)
        self.d20.setIcon(QIcon("assets/d20.png"))
        self.d20.clicked.connect(self.d20clicked)
        self.percentile = QPushButton("percentile")
        self.percentile.setFixedHeight(88)
        self.percentile.setIcon(QIcon("assets/percentile.png"))
        self.percentile.clicked.connect(self.percentileclicked)

        # placeholder button for all button needs
        self.bb = QPushButton("this is just a button")

        # output and empty qlabel to be updated
        outt = QLabel("Outcome of last dice roll:")
        self.outn = QLabel("") # starts empty, updates with each roll
        self.outn.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # output hbox
        output = QHBoxLayout()
        output.addWidget(outt)
        output.addWidget(self.outn)

        # first row of dice: d4, d6, and d8
        h1 = QHBoxLayout()
        h1.addWidget(self.d4)
        h1.addWidget(self.d6)
        h1.addWidget(self.d8)

        # second row of dice: d10, d12, d20
        h2 = QHBoxLayout()
        h2.addWidget(self.d10)
        h2.addWidget(self.d12)
        h2.addWidget(self.d20)

        # assembles dice grid and output on bottom
        v1 = QVBoxLayout()
        v1.addLayout(h1)
        v1.addLayout(h2)
        v1.addWidget(self.percentile)
        v1.addLayout(output)

        # widget wrapper for the first vbox
        w1 = QWidget()
        w1.setLayout(v1)

        #################### SECOND INTERFACE START ####################

        # input stuff
        rule = QLabel("Enter dice in [x]d[y]+[mod] format. Integers limited to range 1-999.")
        num = QLabel("Number of dice:")
        v = QIntValidator()
        v.setBottom(1) # 000 would be an intermediate value, caught in the roll function
        self.getnum = QLineEdit()
        self.getnum.setMaxLength(3)
        self.getnum.setPlaceholderText("Enter a positive integer.")
        self.getnum.setValidator(v)
        nums = QHBoxLayout()
        nums.addWidget(num)
        nums.addWidget(self.getnum)
        side = QLabel("Number of sides:")
        self.getside = QLineEdit()
        self.getside.setMaxLength(3)
        self.getside.setPlaceholderText("Enter a positive integer.")
        self.getside.setValidator(v)
        sides = QHBoxLayout()
        sides.addWidget(side)
        sides.addWidget(self.getside)
        mod = QLabel("Modifier:")
        w = QIntValidator()
        w.setRange(-999, 999)
        self.getmod = QLineEdit()
        self.getmod.setMaxLength(4)
        self.getmod.setPlaceholderText("Enter a positive or negative integer.")
        self.getmod.setValidator(w)
        mods = QHBoxLayout()
        mods.addWidget(mod)
        mods.addWidget(self.getmod)

        # button to roll
        self.rollb = QPushButton("Roll custom dice!")
        self.rollb.clicked.connect(self.roll)
        self.rollb.setFixedHeight(88)

        # output and empty qlabel to be updated
        outt2 = QLabel("Outcome of last dice roll:")
        self.outn2 = QLabel("") # starts empty, updates with each roll
        self.outn2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # output hbox
        output2 = QHBoxLayout()
        output2.addWidget(outt2)
        output2.addWidget(self.outn2)

        # assembles the custom dice interface
        v2 = QVBoxLayout()
        v2.addStretch()
        v2.addLayout(nums)
        v2.addStretch()
        v2.addLayout(sides)
        v2.addStretch()
        v2.addLayout(mods)
        v2.addStretch()
        v2.addWidget(self.rollb)
        v2.addStretch()
        v2.addLayout(output2)
        v2.addStretch()

        # widget wrapper for the second vbox
        w2 = QWidget()
        w2.setLayout(v2)

        #################### DISPLAY SECTION ####################

        # tabbing display between standard and custom dice
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.North)
        tabs.setMovable(True)
        tabs.addTab(w1, "Standard dice")
        tabs.addTab(w2, "Custom dice")

        # makes the window
        self.setStyleSheet("""background-color: pink;""")
        self.setWindowTitle("Dice Roller")
        self.setFixedSize(QSize(300, 400))
        self.setCentralWidget(tabs)
        
    def d4clicked(self):
        outcome = random.randint(1, 4)
        with open("logfiles/TemporaryLog.txt", "a") as log:
            log.write("rolled 1d4+0 --> {} \n".format(outcome))
        print("log: rolled 1d4+0 -->", outcome)
        self.outn.setText(str(outcome))
        self.outn2.setText(str(outcome))

    def d6clicked(self):
        outcome = random.randint(1, 6)
        with open("logfiles/TemporaryLog.txt", "a") as log:
            log.write("rolled 1d6+0 --> {} \n".format(outcome))
        print("log: rolled 1d6+0 -->", outcome)
        self.outn.setText(str(outcome))
        self.outn2.setText(str(outcome))

    def d8clicked(self):
        outcome = random.randint(1, 8)
        with open("logfiles/TemporaryLog.txt", "a") as log:
            log.write("rolled 1d8+0 --> {} \n".format(outcome))
        print("log: rolled 1d8+0 -->", outcome)
        self.outn.setText(str(outcome))
        self.outn2.setText(str(outcome))

    def d10clicked(self):
        outcome = random.randint(1, 10)
        with open("logfiles/TemporaryLog.txt", "a") as log:
            log.write("rolled 1d10+0 --> {} \n".format(outcome))
        print("log: rolled 1d10+0 -->", outcome)
        self.outn.setText(str(outcome))
        self.outn2.setText(str(outcome))

    def d12clicked(self):
        outcome = random.randint(1, 12)
        with open("logfiles/TemporaryLog.txt", "a") as log:
            log.write("rolled 1d12+0 --> {} \n".format(outcome))
        print("log: rolled 1d12+0 -->", outcome)
        self.outn.setText(str(outcome))
        self.outn2.setText(str(outcome))

    def d20clicked(self):
        outcome = random.randint(1, 20)
        with open("logfiles/TemporaryLog.txt", "a") as log:
            log.write("rolled 1d20+0 --> {} \n".format(outcome))
        print("log: rolled 1d20+0 -->", outcome)
        self.outn.setText(str(outcome))
        self.outn2.setText(str(outcome))

    def percentileclicked(self):
        outcome = random.randint(1, 100)
        with open("logfiles/TemporaryLog.txt", "a") as log:
            log.write("rolled percentile dice --> {}% \n".format(outcome))
        print("log: rolled percentile dice --> ", outcome, "%", sep="")
        self.outn.setText(str(outcome) + "%")
        self.outn2.setText(str(outcome) + "%")

    def roll(self):
        x = self.getnum.text()
        if x in ("", "0", "00", "000"):
            a1 = QMessageBox(self)
            a1.setWindowTitle("Bad input :(")
            a1.setIcon(QMessageBox.Icon.Warning)
            a1.setText("Number of dice cannot be 0 empty!")
            a1.exec()
            return
        else:
            x = int(x)
        y = self.getside.text()
        if y in ("", "0", "00", "000"):
            a2 = QMessageBox(self)
            a2.setWindowTitle("Bad input :(")
            a2.setText("Number of sides cannot be 0 or empty!")
            a2.exec()
            return
        else:
            y = int(y)
        m = self.getmod.text()
        if m == "":
            m = 0
        else:
            m = int(m)
        outcome = 0
        for i in range(x):
            outcome = outcome + random.randint(1, y)
        outcome = outcome + m
        with open("logfiles/TemporaryLog.txt", "a") as log:
            log.write("rolled {}d{}+{} --> {} \n".format(x, y, m, outcome))
        print("log: rolled ", x, "d", y, "+", m, " --> ", outcome, sep="")
        self.outn.setText(str(outcome))
        self.outn2.setText(str(outcome))

# class start(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.dr = None # at start of program no widget state is recorded
        
#         self.button = QPushButton("Open dice roller widget")
#         self.button.clicked.connect(self.clicked)
        
#         self.setWindowTitle("Start Page")
#         self.setCentralWidget(self.button)
        
#     def clicked(self):
#         if self.dr is None: # if no widget state saved, creates widget
#             self.dr = DiceRoller()
#         self.dr.show()


# app = QApplication([])

# window = start()
# window.show()

# app.exec()

import os
import sys
from json import load, dump
from subprocess import call
from ctypes import windll
from string import ascii_uppercase as uppercase
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QListWidget, QLabel,
                             QGroupBox, QHBoxLayout, QPushButton, QVBoxLayout, QRadioButton)

class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        #Set layout
        layout = QGridLayout()
        self.setLayout(layout)

        #Configure widget with settings and graphics
        self.setFixedSize(500, 350)
        self.setWindowIcon(QIcon(resource_path("assets\\icons\\CnC3 - Gold.ico")))
        self.setWindowTitle("Medstar117's CNC3 Mod Launcher")
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.MSWindowsFixedSizeDialogHint)

        #Initialize UI data
        self.selectedGame = "Tiberium Wars"
        self.selectedMod = None
        self.listwidget = QListWidget()
        self.logo = QLabel()
        self.buttonGroup = self.createGroup("Buttons")
        self.modbutton = self.buttonGroup.findChildren(QPushButton)[0]

        #Set and display UI data to widget
        self.logo.setPixmap(QPixmap(resource_path("assets\\images\\banner.PNG")))
        layout.addWidget(self.logo, 0, 0, 1, 2)
        layout.addWidget(self.createGroup("Games"), 1, 0)
        layout.addWidget(self.createGroup("Mods"), 1, 1)
        layout.addWidget(self.buttonGroup, 2, 0, 1, 2)

    def setListItems(self, items):
        """Puts all available mods into the listwidget for selection"""
        self.listwidget.clear()
        self.selectedMod = None
        self.modbutton.setEnabled(False)

        for i in range(len(items)):
            self.listwidget.insertItem(i, items[i])

    def createGroup(self, name):
        """Create a QGroupBox with necessary buttons for needed purpose"""
        groupBox = QGroupBox()
        if name != "Buttons":
            box = QVBoxLayout()
        else:
            box = QHBoxLayout()

        if name == "Games":
            groupBox.setTitle(name)
            titles = ["Tiberium Wars", "Kanes Wrath"]
            buttons = [QRadioButton(title) for title in titles]
            buttons[0].setChecked(True)
            for button in buttons:
                button.title = titles[buttons.index(button)]
                button.toggled.connect(self.radioClicked)
                box.addWidget(button)
            box.addStretch(1)

        elif name == "Mods":
            groupBox.setTitle(name + " - Located at {}".format(mods_path))
            self.setListItems(tiberium_mods)
            self.listwidget.clicked.connect(self.listClicked)
            box.addWidget(self.listwidget)
            box.addStretch(1)

        elif name == "Buttons":
            labels = ["Play Mod", "Play Vanilla"]
            buttons = [QPushButton(label) for label in labels]
            for button in buttons:
                button.clicked.connect(self.install_playGame)
                box.addWidget(button)
            buttons[0].setEnabled(False)

        groupBox.setLayout(box)

        return groupBox

    def listClicked(self, qmodelindex):
        """Sets the selected mod, and ensures the mod button is enabled"""
        self.selectedMod = self.listwidget.currentItem().text()
        if self.modbutton.isEnabled != True:
            self.modbutton.setEnabled(True)

    def radioClicked(self):
        """Set available mods to screen for desired game"""
        radioButton = self.sender()
        if radioButton.isChecked():
            if radioButton.title == "Tiberium Wars":
                self.setListItems(tiberium_mods)
                self.selectedGame = "Tiberium Wars"
            elif radioButton.title == "Kanes Wrath":
                self.setListItems(kane_mods)
                self.selectedGame = "Kanes Wrath"

    def install_playGame(self):
        """Checks which button is selected by user and either:
        1) Installs the selected game and launches 'CNC3Launcher.exe' or
        2) Restores the retail .SkuDef file and launches 'CNC3Launcher.exe'"""
        def _restoreSkuDef():
            """Restores the retail .SkuDef file"""
            with open(os.path.join(skudef_path, skudef_file), "w") as f:
                f.writelines(orig_skudef_lang_data)

        def _findSkuDefs(walks):
            """Finds all .SkuDef files for the selected mod"""
            for walk in walks:
                for file in walk[2]:
                    if file.lower().endswith("skudef"):
                        yield os.path.join(os.path.abspath(walk[0]), file)

        def _install():
            """Installs the selected mod"""
            mod = os.path.join(modpath, self.selectedMod)
            walks = [item for item in os.walk(mod)]
            skudef_files = [file for file in _findSkuDefs(walks)]

            _restoreSkuDef()

            with open(os.path.join(skudef_path, skudef_file), "w") as f:
                for file in skudef_files:
                    f.write("add-config {}\n".format(file))
                f.writelines(orig_skudef_lang_data)

        def _startGame():
            """Runs 'CNC3Launcher.exe'"""
            if self.selectedGame == "Tiberium Wars" or "Kanes Wrath":
                os.chdir(launcher_path)
                call("CNC3Launcher.exe")

        #TODO: Write this data to an existing "path.info" file?
        #TODO: Expect language files other than "CNC3_english_1.9.SkuDef" (e.g. "CNC3_french_1.9.SkuDef", etc.)
        if self.selectedGame == "Tiberium Wars":
            modpath = tiberium_mods_path
            skudef_file = "CNC3_english_1.9.SkuDef"
            orig_skudef_lang_data = ["set-exe RetailExe\\1.9\\cnc3game.dat\n",
                                    "add-config Lang-english\\1.9\\config.txt\n",
                                    "add-config EnglishAudio\\1.7\\config.txt\n",
                                    "add-config Movies\\1.0\\config.txt\n",
                                    "add-config Core\\1.9\\config.txt\n",
                                    "add-config SP\\1.9\\config.txt\n",
                                    "add-config MP\\1.9\\config.txt\n",
                                    "add-config RetailExe\\1.9\\config.txt\n",
                                    "add-search-path big:\n\n"]

        elif self.selectedGame == "Kanes Wrath":
            modpath = kane_mods_path
            skudef_file = "CNC3EP1_english_1.2.SkuDef"
            orig_skudef_lang_data = ["set-exe RetailExe\\1.2\\cnc3ep1.dat\n",
                                    "add-config Lang-english\\1.2\\config.txt\n",
                                    "add-config EnglishAudio\\1.2\\config.txt\n",
                                    "add-config Core\\1.2\\config.txt\n",
                                    "add-config Meta\\1.2\\config.txt\n",
                                    "add-config RetailExe\\1.2\\config.txt\n",
                                    "add-config Movies\\1.0\\config.txt\n",
                                    "add-search-path big:\n\n"]

        button_name = self.sender().text()
        skudef_path = os.path.join(launcher_path, "Command Conquer 3 {}".format(self.selectedGame))

        if button_name == "Play Mod":
            _install()
            _startGame()
        elif button_name == "Play Vanilla":
            _restoreSkuDef()
            _startGame()

def find_launcher():
    """Find retail CNC3 game launcher"""
    def _find_drives():
        """Finds all connected drives"""
        drives = []
        bitmask = windll.kernel32.GetLogicalDrives()
        for letter in uppercase:
            if bitmask & 1:
                drives.append(letter)
            bitmask >>= 1
        return drives

    for drive in _find_drives():
        for r,d,f in os.walk(drive + ":/"):
            for file in f:
                if file == "CNC3Launcher.exe":
                    return os.path.abspath(r)

def resource_path(relative_path):
    """Get absolute path to needed resource"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    #Set needed paths to variables.
    mods_path = os.path.join(os.path.expanduser("~"), "Documents", "CNC3 Mods")
    tiberium_mods_path = os.path.join(mods_path, "Tiberium Wars")
    kane_mods_path = os.path.join(mods_path, "Kanes Wrath")

    #Check if expeted paths exist; if not, create them.
    main_paths = [mods_path, tiberium_mods_path, kane_mods_path]
    for path in main_paths:
        if os.path.exists(path) == False:
            os.mkdir(path)

    #Check if the launcher had ran before and had stored where "CNC3Launcher.exe" is located;
    #If the file doesn't exist, create it and store the data.
    #TODO: Check if data is present; if not, act as if the file doesn't exist or something
    data_path = os.path.join(os.getcwd(), "path.info")
    if os.path.exists(data_path) == True:
        with open(data_path, "r") as f:
            data = load(f)
            launcher_path = data["launcher_path"]
    else:
        data = {"launcher_path": find_launcher()}
        with open(data_path, "w") as f:
            dump(data, f, indent=2)

    #Find all mods in the expected directories and store them into variables
    tiberium_mods = [d for r,d,f in os.walk(tiberium_mods_path)][0]
    kane_mods = [d for r,d,f in os.walk(kane_mods_path)][0]

    #Execute QApplication
    app = QApplication(sys.argv)
    screen = Window()
    screen.show()
    sys.exit(app.exec_())

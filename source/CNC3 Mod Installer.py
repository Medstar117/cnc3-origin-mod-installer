import os
import sys
from json import load, dump
from subprocess import call
from ctypes import windll
from string import ascii_uppercase as uppercase
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QListWidget, QLabel,
                             QGroupBox, QHBoxLayout, QPushButton, QVBoxLayout, QRadioButton)

class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        
        layout = QGridLayout()
        self.setLayout(layout)

        self.setWindowTitle("Medstar117's CNC3 Mod Launcher")
        self.setFixedSize(500, 350)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.MSWindowsFixedSizeDialogHint)
        
        self.selectedGame = "Tiberium Wars"
        self.selectedMod = None
        self.listwidget = QListWidget()
        self.logo = QLabel()
        self.buttonGroup = self.createGroup("Buttons")
        self.modbutton = self.buttonGroup.findChildren(QPushButton)[0]

        self.logo.setPixmap(QPixmap(resource_path("assets\\images\\banner.PNG")))
        layout.addWidget(self.logo, 0, 0, 1, 2)
        layout.addWidget(self.createGroup("Games"), 1, 0)
        layout.addWidget(self.createGroup("Mods"), 1, 1)
        layout.addWidget(self.buttonGroup, 2, 0, 1, 2)
        
    def setListItems(self, items):
        self.listwidget.clear()
        self.selectedMod = None
        self.modbutton.setEnabled(False)
        
        for i in range(len(items)):
            self.listwidget.insertItem(i, items[i])

    def createGroup(self, name):
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

    def install_playGame(self):
        def _cleanDir():
            skudef_dir = [item for item in os.walk(skudef_path)][0]
            config_big_dir = [item for item in os.walk(config_and_big_path)][0]
            for file in skudef_dir[2]:
                if file not in orig_skudef_path_files:
                    os.remove(os.path.join(skudef_dir[0], file))
            for file in config_big_dir[2]:
                if file not in orig_config_and_big_path_files:
                    os.remove(os.path.join(config_big_dir[0], file))

            with open(os.path.join(config_and_big_path, orig_config_and_big_path_files[0]), "w") as f:
                f.writelines(orig_config_data)
        
        def _findFiles(walks, type):
            for walk in walks:
                for file in walk[2]:
                    if file.endswith(type):
                        yield os.path.join(os.path.abspath(walk[0]), file)
            
        def _install():
            mod = os.path.join(modpath, self.selectedMod)
            walks = [item for item in os.walk(mod)]   
            skudef_files = [file for file in _findFiles(walks, "skudef")]
            big_files = [file for file in _findFiles(walks, "big")]

            _cleanDir()
            
            for file in skudef_files:
                call(["copy", file, skudef_path], shell=True)

            with open(os.path.join(config_and_big_path, "config.txt"), "w") as f:
                config_data = [orig_config_data[0]]
                for file in big_files:
                    config_data.append("add-big {}\n".format(os.path.basename(file)))
                    call(["copy", file, config_and_big_path], shell=True)
                config_data.append(orig_config_data[1])
                f.writelines(config_data)
            
        def _startGame():
            if self.selectedGame == "Tiberium Wars" or "Kanes Wrath":
                os.chdir(launcher_path)
                call("CNC3Launcher.exe")

        if self.selectedGame == "Tiberium Wars":
            coreFolder = "1.9"
            modpath = tiberium_mods_path
            orig_skudef_path_files = ['CNC3.exe', 'CNC3.par', 'CNC3_english_1.9.SkuDef',
                                      'LauncherSupport.dat', 'patchw32.dll', 'VistaShellSupport.dll']
            orig_config_and_big_path_files = ["config.txt", "patch9.big"]
            orig_config_data = ["add-big patch9.big\n", "add-config ..\\1.8\\config.txt"]
        elif self.selectedGame == "Kanes Wrath":
            coreFolder = "1.2"
            modpath = kane_mods_path
            orig_skudef_path_files = ["CNC3EP1.exe", "CNC3EP1.par", "CNC3EP1_english_1.2.SkuDef",
                                      "CnC3-KW.jpg", "LauncherSupport.dat", "patchw32.dll",
                                      "VistaShellSupport.dll"]
            orig_config_and_big_path_files = ["config.txt", "patch2.big"]
            orig_config_data = ["add-big patch2.big\n", "add-config ..\\1.1\\config.txt"]
            
        button_name = self.sender().text()
        skudef_path = os.path.join(launcher_path, "Command Conquer 3 {}".format(self.selectedGame))
        config_and_big_path = os.path.join(skudef_path, "Core", coreFolder)
        
        if button_name == "Play Mod":
            _install()
            _startGame()
        elif button_name == "Play Vanilla":
            _cleanDir()
            _startGame()
        
    def listClicked(self, qmodelindex):
        self.selectedMod = self.listwidget.currentItem().text()
        if self.modbutton.isEnabled != True:
            self.modbutton.setEnabled(True)

    def radioClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            if radioButton.title == "Tiberium Wars":
                self.setListItems(tiberium_mods)
                self.selectedGame = "Tiberium Wars"
            elif radioButton.title == "Kanes Wrath":
                self.setListItems(kane_mods)
                self.selectedGame = "Kanes Wrath"

def find_launcher():
    def _find_drives():
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
    """Get absolute path to resource"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
        
    return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    
    mods_path = os.path.join(os.path.expanduser("~"), "Documents", "CNC3 Mods")
    tiberium_mods_path = os.path.join(mods_path, "Tiberium Wars")
    kane_mods_path = os.path.join(mods_path, "Kanes Wrath")

    main_paths = [mods_path, tiberium_mods_path, kane_mods_path]
    for path in main_paths:
        if os.path.exists(path) == False:
            os.mkdir(path)

    data_path = os.path.join(os.getcwd(), "path.info")
    if os.path.exists(data_path) == True:
        with open(data_path, "r") as f:
            data = load(f)
            launcher_path = data["launcher_path"]
    else:
        data = {"launcher_path": find_launcher()}
        with open(data_path, "w") as f:
            dump(data, f, indent=2)

    tiberium_mods = [d for r,d,f in os.walk(tiberium_mods_path)][0]
    kane_mods = [d for r,d,f in os.walk(kane_mods_path)][0]
    app = QApplication(sys.argv)
    screen = Window()
    screen.show()
    sys.exit(app.exec_())

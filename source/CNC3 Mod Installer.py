import os, sys
from json import load, dump
from subprocess import call
from ctypes import windll
from string import ascii_uppercase as uppercase
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QListWidget,
                            QLabel, QGroupBox, QHBoxLayout, QPushButton,
                            QVBoxLayout, QRadioButton)

#GUI Window
class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        #Set Layout
        layout = QGridLayout()
        self.setLayout(layout)

        #Configure widget graphics and static dimensions
        self.setFixedSize(500, 350)
        self.setWindowIcon(QIcon(resource_path("assets\\icons\\CnC3 - Gold.ico")))
        self.setWindowTitle("Medstar117's CNC3 Mod Launcher")
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.MSWindowsFixedSizeDialogHint)

        #Initialize UI data
        self.selectedGame = None
        self.selectedMod = None
        self.listwidget = QListWidget()
        self.logo = QLabel()
        self.buttonGroup = self.createGroup("Buttons")
        self.modbutton = self.buttonGroup.findChildren(QPushButton)[0]

        #Set and display UI data to widget
        self.logo.setPixmap(QPixmap(resource_path("assets\\images\\banner.PNG")))
        layout.addWidget(self.logo, 0, 0, 1, 2) #Logo at top of window
        layout.addWidget(self.createGroup("Games"), 1, 0) #Widget holding game radio buttons
        layout.addWidget(self.createGroup("Mods"), 1, 1) #Widget holding mod list
        layout.addWidget(self.buttonGroup, 2, 0, 1, 2) #Widget holding buttons at bottom of window


    """---------------------------GUI Functions---------------------------"""
    def setListItems(self, items):
        """Displays all available mods into the listwidget for selection."""
        self.listwidget.clear()
        self.selectedMod = None
        self.modbutton.setEnabled(False)

        #Inserts items into list
        for i in range(len(items)):
            self.listwidget.insertItem(i, items[i])

    def createGroup(self, name):
        """Create a QGroupBox with necessary buttons for each game."""
        groupBox = QGroupBox()
        if name != "Buttons": box = QVBoxLayout()
        else: box = QHBoxLayout()

        if name == "Games":
            #Creates container for all game radio buttons
            groupBox.setTitle(name)

            #Only displays a radio button if game is installed
            installed_titles = [game_data[supported_games[i]]["Name"]
                                for i in range(supported_games_count)
                                if game_data[supported_games[i]]["Launcher Path"] != False]

            buttons = [QRadioButton(title) for title in installed_titles]
            buttons[0].setChecked(True)
            for button in buttons:
                button.title = installed_titles[buttons.index(button)]
                button.toggled.connect(self.radioClicked)
                box.addWidget(button)
            box.addStretch(1)
            self.selectedGame = buttons[0].title

        elif name == "Mods":
            #Creates container for mod list
            groupBox.setTitle(name + " - Located at {}".format(cnc_mods_path))
            self.setListItems(game_data[self.selectedGame]["Mods"])
            self.listwidget.clicked.connect(self.listClicked)
            box.addWidget(self.listwidget)
            box.addStretch(1)

        elif name == "Buttons":
            #Creates container for GUI buttons
            labels = ["Play Mod", "Play Vanilla"]
            buttons = [QPushButton(label) for label in labels]
            for button in buttons:
                button.clicked.connect(self.install_playGame)
                box.addWidget(button)
            buttons[0].setEnabled(False)

        groupBox.setLayout(box)
        return groupBox

    def listClicked(self, qmodelindex):
        """Sets the selected mod and ensures the mod button is enabled."""
        self.selectedMod = self.listwidget.currentItem().text()
        if self.modbutton.isEnabled != True:
            self.modbutton.setEnabled(True)

    def radioClicked(self):
        """Set available mods to screen for selected game."""
        radioButton = self.sender()
        game = radioButton.title

        if radioButton.isChecked():
            self.setListItems(game_data[game]["Mods"])
            self.selectedGame = game

    def install_playGame(self):
        """Check selected mod and either install the mod or restore the retail
        .SkuDef file before launching the appropriate executable."""

        def _restoreSkuDef():
            """Restores the retail .SkuDef file."""
            with open(skudef_file, "w") as skudef:
                skudef.writelines(orig_skudef_lang_data)

        def _findSkuDefs(walks):
            """Finds all .SkuDef files for the selected mod."""
            for walk in walks:
                for file in walk[2]:
                    if file.lower().endswith("skudef"):
                        yield os.path.join(os.path.abspath(walk[0]), file)

        def _install_mod():
            """Installs the selected mod."""
            mod = os.path.join(modpath, self.selectedMod)
            walks = [item for item in os.walk(mod)]
            mod_skudefs = [file for file in _findSkuDefs(walks)]

            _restoreSkuDef()

            with open(skudef_file, "w") as skudef:
                for file in mod_skudefs:
                    skudef.write("add-config {}\n".format(file))
                skudef.writelines(orig_skudef_lang_data)

        def _startGame():
            """Runs the appropriate game executable."""
            if self.selectedGame == "Tiberium Wars" or "Kanes Wrath":
                if game_data["Origin"]["Launcher Path"] != False:
                    os.chdir(game_data["Origin"]["Launcher Path"])
                    call(game_data["Origin"]["EXE Name"])
                else:
                    os.chdir(game_data[self.selectedGame]["Launcher Path"])
                    game_exe = game_data[self.selectedGame]["EXE Name"]
                    if os.path.exists(game_exe):
                        call(game_exe)
                    else:
                        call(game_exe.lower())


        #TODO: Expect language files other than "CNC3_english_1.9.SkuDef"
        #(e.g. "CNC3_french_1.9.SkuDef", etc.)
        button_name = self.sender().text()
        modpath = game_data[self.selectedGame]["Mod Path"]
        orig_skudef_lang_data = game_data[self.selectedGame]["Skudef Data"]
        skudef_file = os.path.join(game_data[self.selectedGame]["Launcher Path"],
                                   game_data[self.selectedGame]["Skudef Name"])

        if button_name == "Play Mod":
            _install_mod()
            _startGame()
        elif button_name == "Play Vanilla":
            _restoreSkuDef()
            _startGame()


"""---------------------------Non-GUI Functions---------------------------"""
def resource_path(relative_path):
    """Get absolute path to needed resource."""
    try: base_path = sys._MEIPASS
    except AttributeError: base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#def find_launcher(launcher_name):
def find_launchers():
    """Automatically finds specified executable name."""

    def _find_drives():
        """Automatically finds all connected drives (Windows)."""
        drives = []
        bitmask = windll.kernel32.GetLogicalDrives()
        for letter in uppercase:
            if bitmask & 1:
                drives.append(letter)
            bitmask >>= 1
        return drives

    #Search for executable among connected drives, return the directory it is in
    exe_paths = {}
    names = exe_names.copy()
    for drive in _find_drives():
        for r, d, f in os.walk(drive + ":/"):
            for file in f:
                for name in names:
                    if file == name or file == name.lower():
                        exe_paths.update({name : os.path.abspath(r)})
                        names.remove(name)
                    if len(names) == 0:
                        break

    if len(names) != 0:
        for name in names:
            exe_paths.update({name : False})

    return exe_paths #No executable is found

def fetch_mods(path):
    return [d for r, d, f in os.walk(path)][0]

"""------------------------Main Loop Initialization------------------------"""
if __name__ == "__main__":
    #General data
    launcher_names = ["origin_launcher_path", "tiberium_launcher_path", "kane_launcher_path"]
    exe_names = ["CNC3Launcher.exe", "CNC3.exe", "CNC3EP1.exe"]
    supported_games = ["Tiberium Wars", "Kanes Wrath"]
    supported_games_count = len(supported_games)

    #Set mod paths
    cnc_mods_path = os.path.join(os.path.expanduser("~"), "Documents", "CNC Mods")
    tiberium_mods_path = os.path.join(cnc_mods_path, "Tiberium Wars")
    kane_mods_path = os.path.join(cnc_mods_path, "Kanes Wrath")
    mod_paths = [tiberium_mods_path, kane_mods_path]

    #Check if expected paths exist; if not, create them.
    for path in mod_paths:
        if os.path.exists(path) == False:
            os.makedirs(path)

    #Check if the launcher has ran before; there will be a path.info file in
    #the launcher's directory if that is true. If the launcher has not been ran
    #before, find all game executable locations.
    path_info = os.path.join(os.getcwd(), "path_locations.info")
    if os.path.exists(path_info) == True:
        with open(path_info, "r") as data:
            paths = load(data)
        launcher_paths = [paths[name] for name in launcher_names]#Origin, Tiberium, Kane
    else:
        launcher_dict = find_launchers()
        launcher_paths = [launcher_dict[exe] for exe in exe_names]
        json_data = dict(zip(launcher_names, launcher_paths))

        with open(path_info, "w") as path_file:
            dump(json_data, path_file, indent = 2)

    #Load original skudef info
    skudef_info = resource_path("assets\\data\\skudef_info.json")
    with open(skudef_info, "r") as info:
        skudef_attrs = load(info)

    #Find all mods in the expected directories and store their paths into lists
    #and load the needed skudef path
    available_mods = [fetch_mods(path) for path in mod_paths]#Tiberium, Kane

    #Config Data
    game_info = resource_path("assets\\data\\game_data.json")
    with open(game_info, "r") as info:
        game_data = load(info)

    for game_key in game_data.keys():
        for item in game_data[game_key].keys():
            game_data[game_key][item] = eval(game_data[game_key][item])

    #Execute QApplication
    app = QApplication(sys.argv)
    screen = Window()
    screen.show()
    sys.exit(app.exec_())

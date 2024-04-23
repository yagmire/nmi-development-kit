import sys, py7zr, json, os, shutil
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QFrame, QMessageBox

def pack(name=None, folder=None, exe=None, version=None):
    info_template_json = {
        "name": name,
        "execname": os.path.basename(exe),
        "nmi-version": version
    }
    with open('nmi.iinfo', 'w') as nmi_iinfo:
        json.dump(info_template_json, nmi_iinfo, indent=4)
    print("Created iinfo.")
    shutil.move("nmi.iinfo",f"{folder}")
    print("\nPacking game with Name:", name, "\nFolder:", folder, "\nEXE File:", exe, "\nVersion:", version)
    with py7zr.SevenZipFile(f"{name}.nmi", 'w', password=r"m1FC%0%0", header_encryption=True) as archive:
        orig_dir = os.getcwd()
        os.chdir(f"{os.path.dirname(folder)}")
        archive.writeall(f"{os.path.basename(folder)}/")
        os.chdir(orig_dir)
    print(f"\nPacking of '{name}' has finished.")
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(f"The packing of '{name}' has finished!")
    msg.setInformativeText(f"You can find '{name}.nmi' in {os.getcwd()} You can share this file for others to install.")
    msg.setWindowTitle("NMI Publisher Kit")
    msg.setStandardButtons(QMessageBox.Ok)
    retval = msg.exec_()

class NMI_Publishing_Kit(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('NMI Publishing Kit')

        self.name_label = QLabel('Enter in the name of game you want to publish:')
        self.name_input = QLineEdit()

        self.folder_label = QLabel('Select the folder containing the game files (the folder name must be the same as the game name):')
        self.folder_button = QPushButton('Browse')
        self.folder_button.clicked.connect(self.openFolderDialog)
        self.folder_path_label = QLabel()

        self.exe_label = QLabel('Select EXE File that runs the game (inside the game folder, do not use a shortcut):')
        self.exe_button = QPushButton('Browse')
        self.exe_button.clicked.connect(self.openExeDialog)
        self.exe_path_label = QLabel()

        self.version_label = QLabel('NMI Version (e.g. \'v1.0\'):')
        self.version_input = QLineEdit()

        self.pack_button = QPushButton('Pack My Game!')
        self.pack_button.clicked.connect(self.packGame)

        # Add separators
        separator1 = QFrame()
        separator1.setFrameShape(QFrame.HLine)
        separator1.setFrameShadow(QFrame.Sunken)

        separator2 = QFrame()
        separator2.setFrameShape(QFrame.HLine)
        separator2.setFrameShadow(QFrame.Sunken)

        separator3 = QFrame()
        separator3.setFrameShape(QFrame.HLine)
        separator3.setFrameShadow(QFrame.Sunken)

        vbox = QVBoxLayout()
        vbox.addWidget(self.name_label)
        vbox.addWidget(self.name_input)
        vbox.addWidget(separator1)
        vbox.addWidget(self.folder_label)
        vbox.addWidget(self.folder_button)
        vbox.addWidget(self.folder_path_label)
        vbox.addWidget(separator2)
        vbox.addWidget(self.exe_label)
        vbox.addWidget(self.exe_button)
        vbox.addWidget(self.exe_path_label)
        vbox.addWidget(separator3)
        vbox.addWidget(self.version_label)
        vbox.addWidget(self.version_input)
        vbox.addWidget(self.pack_button)

        self.setLayout(vbox)
        self.show()

    def openFolderDialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folder_path:
            self.folder_path_label.setText(folder_path)

    def openExeDialog(self):
        exe_file, _ = QFileDialog.getOpenFileName(self, 'Select EXE File', filter='Executable (*.exe)')
        if exe_file:
            self.exe_path_label.setText(exe_file)

    def packGame(self):
        name = self.name_input.text()
        folder = self.folder_path_label.text()
        exe_file = self.exe_path_label.text()
        version = self.version_input.text()
        # Perform packing operation with the provided inputs
        pack(name, folder, exe_file, version)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = NMI_Publishing_Kit()
    sys.exit(app.exec_())

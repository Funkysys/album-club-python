from pathlib import Path
from PySide6 import QtWidgets, QtCore
import json

def createBandyAndFile():
    path = Path.cwd() / "data"
    path.mkdir(exist_ok=True)
    path = path / "Albums.json"

    if not path.exists() or path.stat().st_size == 0:
        with open(path, "w") as file:
            json.dump([], file) 

    try:
        with open(path, "r") as file:
            json.load(file) 
    except json.JSONDecodeError:
        with open(path, "w") as file:
            json.dump([], file)

def add_albums_to_list_widget(self, album):    
    lw_item = QtWidgets.QListWidgetItem(str(album))
    lw_item.setData(QtCore.Qt.ItemDataRole.UserRole, album)
    self.lw_albums_list.addItem(lw_item)

def empty_input_fields(self):
    self.le_album_to_add.clear()
    self.le_year_to_add.clear()
    self.le_band_to_add.clear()
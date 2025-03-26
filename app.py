from PySide6 import QtWidgets, QtCore
from album import Album, get_albums, clear_albums
from utils import add_albums_to_list_widget, createBandyAndFile, empty_input_fields

class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Album Database")
        self.setup_ui()
        self.setup_css()
        self.setup_connections()

    def setup_ui(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.le_album_to_add = QtWidgets.QLineEdit(self, placeholderText="Album Title")
        self.le_year_to_add = QtWidgets.QLineEdit(self, placeholderText="Year")
        self.le_band_to_add = QtWidgets.QLineEdit(self, placeholderText="Band")
        self.pb_add_album_button = QtWidgets.QPushButton("Add Album", self)
        self.lw_albums_list = QtWidgets.QListWidget(self)
        self.lw_albums_list.setSelectionMode(QtWidgets.QListWidget.SelectionMode.MultiSelection)
        self.pb_delete_album_button = QtWidgets.QPushButton("Delete Album(s)", self)
        self.pb_clear_albums_button = QtWidgets.QPushButton("Clear albums", self)

        self.main_layout.addWidget(self.le_album_to_add)
        self.main_layout.addWidget(self.le_year_to_add)
        self.main_layout.addWidget(self.le_band_to_add)
        self.main_layout.addWidget(self.pb_add_album_button)
        self.main_layout.addWidget(self.lw_albums_list)
        self.main_layout.addWidget(self.pb_delete_album_button)
        self.main_layout.addWidget(self.pb_clear_albums_button)

        self.populate_albums()

    def setup_css(self):
        self.setStyleSheet("""
            background-color:
            rgb(30, 30, 30);
            color: white;
            border: 1px solid lightgrey;
            border-radius: 5px;
            padding: 5px;
        """)

    def setup_connections(self):
        self.pb_add_album_button.clicked.connect(self.add_album)
        self.le_band_to_add.returnPressed.connect(self.add_album)
        self.pb_delete_album_button.clicked.connect(self.remove_album)
        self.pb_clear_albums_button.clicked.connect(self.clear_albums)

    def populate_albums(self):
        albums = get_albums() or []
        for album in albums:
            add_albums_to_list_widget(self, album)

    def add_album(self):
        albums_list = self.le_album_to_add.text()
        year_list = self.le_year_to_add.text()
        band_list = self.le_band_to_add.text()
        if not albums_list:
            return False
        if not year_list:
            return False
        if not band_list:
            return False
        album = Album(albums_list, year_list, band_list)
        result = album.add_albums()
        if result:
            add_albums_to_list_widget(self, album)
            empty_input_fields(self)
            self._refresh_albums()
            return True
        return False 

    def remove_album(self):
        selected_items = self.lw_albums_list.selectedItems()
        if not selected_items:
            print("No items selected")
            return False

        for album_item in selected_items:
            album = album_item.data(QtCore.Qt.ItemDataRole.UserRole)
            
            if not album:
                print(f"Album data is None for item: {album_item.text()}")  # Ajout d'un debug print
                return False

            album.delete_album()

            print(f"Deleting album: {album.title}")
            row = self.lw_albums_list.row(album_item)
            self.lw_albums_list.takeItem(row)

        self.lw_albums_list.clearSelection()
        self._refresh_albums()
        return True

    def clear_albums(self):
        clear_albums()
        self._refresh_albums()

    def _refresh_albums(self):
        self.lw_albums_list.clear()
        albums = get_albums() or []
        for album in albums:
            add_albums_to_list_widget(self, album)
    
    def show(self):
        super().show()



def main():
    createBandyAndFile()
    app = QtWidgets.QApplication([])
    window = App()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
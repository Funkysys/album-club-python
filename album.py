from pathlib import Path
import json
import logging

DATA_FILE = Path.cwd() / "data" / "albums.json"

def get_albums():
    if DATA_FILE.exists():
        try: 
            with open(DATA_FILE, "r") as file:
                all_albums = json.load(file)
            all_albums = [Album(album["title"], album["year"], album["band"]) for album in all_albums]
            if not all_albums:
                logging.warning("No albums in the database.")
                return []
            return all_albums
        except json.JSONDecodeError:
            logging.error(f"Error reading {DATA_FILE}.")
            with open(DATA_FILE, "w") as file:
                json.dump([], file)
def clear_albums():
    if DATA_FILE.exists():
        with open(DATA_FILE, "w") as file:
            json.dump([], file)
        return True
    return False

class Album:
    def __init__(self, title, year, band):
        self.title = title.title()
        self.year = year
        self.band = band

    def __str__(self):
        return f"{self.title} ({self.year}) by {self.band}"

    def __repr__(self):
        return f"album('{self.title}', {self.year}, '{self.band}')"
    
    def _get_albums(self):
        if DATA_FILE.exists():
            with open(DATA_FILE, "r") as file:
                return json.load(file)
        return []
    
    def _write_albums(self, albums):
        with open(DATA_FILE, "w") as file:
            json.dump(albums, file, indent=4)

    def add_albums(self):
        albums = self._get_albums()
        if self.title not in [album["title"] for album in albums]:
            albums.append(self.__dict__)
            self._write_albums(albums)
            return True
        else:
            logging.warning(f"{self.title} already exists in the database.")
            return False

    def delete_album(self):
        if not DATA_FILE.exists():
            logging.warning("No albums in the database.")
            return False
        if not any(album["title"] == self.title for album in self._get_albums()):
            logging.warning(f"{self.title} not found in the database.")
            return False
        albums = self._get_albums()
        albums = [album for album in albums if album["title"] != self.title]
        self._write_albums(albums)
        return True
    
    
        

    

if __name__ == "__main__":
    album = Album("The lord of the rings", 2001, "Peter Jackson")
    album2 = Album("The Matrix", 1999, "Lana Wachowski")
    album3 = Album("The hobbit", 2012, "Peter Jackson")
    album.add_albums()
    album2.add_albums()
    album3.add_albums()
    print(get_albums())
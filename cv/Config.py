class Config:
    def __init__(self):
        self.kandidatennummer = {'top_left': (0, 0), 'bottom_right': (0, 0)}
        self.geburtsdatum = {'top_left': (0, 0), 'bottom_right': (0, 0)}
        self.aufgaben = {'top_left': (0, 0), 'bottom_right': (0, 0)}
        self.erreichte_punktzahl = {'top_left': (0, 0), 'bottom_right': (0, 0)}
        self.schlussnote = {'top_left': (0, 0), 'bottom_right': (0, 0)}


coords = Config()
coords.kandidatennummer['top_left'] = (10, 20)
coords.kandidatennummer['bottom_right'] = (50, 60)

print(coords.kandidatennummer)
# Output: {'top_left': (10, 20), 'bottom_right': (50, 60)}

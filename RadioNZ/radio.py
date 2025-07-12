import tkinter as tk
from configparser import ConfigParser
import vlc
import os

players = {}
favoris = {}
current_station = None

# 📁 Gestion des fichiers INI
def get_folder_path():
    return os.path.join(os.path.expanduser("~"), "Desktop", "RadioNZ")

def load_ini(filename, section):
    config = ConfigParser()
    path = os.path.join(get_folder_path(), filename)
    config.read(path, encoding='utf-8')
    return dict(config.items(section)) if config.has_section(section) else {}

def save_favoris():
    config = ConfigParser()
    config['Favoris'] = favoris
    with open(os.path.join(get_folder_path(), "favoris.ini"), 'w', encoding='utf-8') as f:
        config.write(f)

stations = load_ini("stations.ini", "Stations")
favoris = load_ini("favoris.ini", "Favoris")

# ▶️ Lecture exclusive avec mise à jour du statut
def play_stream(name, source):
    global current_station
    stop_all_streams()
    media = vlc.Media(source)
    players[name].set_media(media)
    players[name].play()
    current_station = name
    update_status()

def stop_all_streams():
    global current_station
    for p in players.values():
        p.stop()
    current_station = None
    update_status()

# 💖 Ajouter aux favoris
def add_favori(name, url):
    if name not in favoris:
        favoris[name] = url
        save_favoris()

# 💔 Retirer des favoris
def remove_favori(name):
    if name in favoris:
        del favoris[name]
        save_favoris()
        favori_window.destroy()
        favori_interface()

# 🎛️ Interface principale
def main_interface():
    global status_label
    root = tk.Tk()
    root.title("Lecteur Radio 🎶")

    for name, url in stations.items():
        players[name] = vlc.MediaPlayer()
        frame = tk.Frame(root)
        frame.pack(fill='x', padx=5, pady=2)

        tk.Label(frame, text=name, width=25, anchor='w').pack(side='left')
        tk.Button(frame, text="▶️ Écouter", command=lambda n=name, u=url: play_stream(n, u)).pack(side='left')
        tk.Button(frame, text="💖 Favori", command=lambda n=name, u=url: add_favori(n, u)).pack(side='left')

    status_label = tk.Label(root, text="⏸️ Rien en lecture en ce moment", fg='blue')
    status_label.pack(pady=(10,0))

    tk.Button(root, text="⏹️ Stop", command=stop_all_streams, fg='white', bg='red').pack(pady=5)
    tk.Button(root, text="🌟 Ouvrir Favoris", command=favori_interface).pack(pady=5)

    root.mainloop()

# 🪟 Fenêtre Favoris avec retrait
def favori_interface():
    global favori_window
    favori_window = tk.Toplevel()
    favori_window.title("Favoris 💖")

    for name, url in favoris.items():
        players[name] = players.get(name, vlc.MediaPlayer())
        frame = tk.Frame(favori_window)
        frame.pack(fill='x', padx=5, pady=2)

        tk.Label(frame, text=name, width=25, anchor='w').pack(side='left')
        tk.Button(frame, text="▶️ Écouter", command=lambda n=name, u=url: play_stream(n, u)).pack(side='left')
        tk.Button(frame, text="🗑️ Supprimer", command=lambda n=name: remove_favori(n)).pack(side='left')

    tk.Button(favori_window, text="⏹️ Stop", command=stop_all_streams, fg='white', bg='red').pack(pady=10)

# 🔁 Mise à jour du statut de lecture
def update_status():
    if current_station:
        status_label.config(text=f"🎵 En lecture : {current_station}")
    else:
        status_label.config(text="⏸️ Rien en lecture en ce moment")

# 🚀 Lancement
main_interface()
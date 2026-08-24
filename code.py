import os
import requests
from pathlib import Path
import ctypes
import time
from colorama import init, Fore, Style

init()

GITHUB_REPO = "kerubim-code/APEX-SETTINGS"
RAW_BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main"

# Liste complète des fichiers locaux (pour réponse "yes")
ALL_LOCAL_FILES = [
    "settings.cfg",
    "videoconfig.txt",
    "voice_volumes.dat"
]

# Liste des fichiers locaux SANS settings.cfg (pour réponse "no")
LOCAL_FILES_NO_SETTINGS = [
    "videoconfig.txt",
    "voice_volumes.dat"
]

PROFILE_FILES = [
    "profile.cfg",
    "steam_autocloud.vdf"
]

STEAM_FILE = {
    "source": "autoexec.cfg",
    "target": "C:/Program Files (x86)/Steam/steamapps/common/Apex Legends/cfg/autoexec.cfg"
}

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_github_raw_url(file_path):
    return f"{RAW_BASE_URL}/{file_path}"

def download_file(url, destination_path):
    try:
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        response = requests.get(url, timeout=10, verify=True)
        response.raise_for_status()
        with open(destination_path, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"Erreur lors du téléchargement de {url}: {e}")
        return False

def download_directory_files(file_list, source_dir, target_dir):
    for filename in file_list:
        source_path = f"{source_dir}/{filename}"
        target_path = os.path.join(target_dir, filename)
        url = get_github_raw_url(source_path)
        if download_file(url, target_path):
            print(f"  ✓ {filename} téléchargé avec succès")
        else:
            print(f"  ✗ Échec du téléchargement de {filename}")

def download_steam_file():
    url = get_github_raw_url(STEAM_FILE["source"])
    if not is_admin():
        print("⚠️ NEED TO RUN IN ADMIN")
        return False
    return download_file(url, STEAM_FILE["target"])

def main():
    username = os.getlogin()
    target_base_dir = Path(f"C:/Users/{username}/Saved Games/Respawn/Apex")

    print("AUTO APEX SETTINGS")
    print("=" * 50)
    print(Fore.GREEN + f"user detect: {username}" + Style.RESET_ALL)
    print(f"detect (utilisateur): {target_base_dir}")
    print(f"detect (Steam): {STEAM_FILE['target']}")
    print("=" * 50)

    # Demande utilisateur
    while True:
        response = input("\nDO YOU WANT THE KEYBIND OF KERUBIMM (if no only videosettings) ? (yes/no) : ").strip().lower()
        if response in ["yes", "no"]:
            break
        print("pls 'yes' or 'no'.")

    # Création du dossier si inexistant
    os.makedirs(target_base_dir, exist_ok=True)

    # Téléchargement des fichiers locaux
    print("\nfolder local...")
    local_files_to_download = ALL_LOCAL_FILES if response == "yes" else LOCAL_FILES_NO_SETTINGS
    download_directory_files(local_files_to_download, "local", target_base_dir / "local")

    # Téléchargement des fichiers de profil
    print("\nfolder profil...")
    download_directory_files(PROFILE_FILES, "profile", target_base_dir / "profile")

    # Téléchargement du fichier Steam
    print("\nfolder Steam...")
    steam_success = download_steam_file()

    # Affichage des fichiers téléchargés
    print("\n" + "=" * 50)
    print("FICHIERS TÉLÉCHARGÉS")
    print("=" * 50)

    print("\nFichiers locaux :")
    local_dir = target_base_dir / "local"
    if local_dir.exists():
        for file in sorted(local_dir.glob('*')):
            print(f"  - {file.name}")

    print("\nFichiers de profil :")
    profile_dir = target_base_dir / "profile"
    if profile_dir.exists():
        for file in sorted(profile_dir.glob('*')):
            print(f"  - {file.name}")

    print("\nFichier Steam :")
    print(f"  - autoexec.cfg -> {STEAM_FILE['target']}")

    print("\n" + Fore.GREEN + "SUCCÈS" + Style.RESET_ALL)
    print(Fore.YELLOW + "\nL'autoclose in 10 secondes..." + Style.RESET_ALL)
    time.sleep(10)

if __name__ == "__main__":
    main()

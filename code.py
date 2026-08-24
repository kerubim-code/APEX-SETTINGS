import os
import requests
from pathlib import Path
import ctypes
import time  # Pour la pause
from colorama import init, Fore, Style

init()

GITHUB_REPO = "kerubim-code/APEX-SETTINGS"
RAW_BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main"

LOCAL_FILES = [
    "settings.cfg",
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
    except:
        return False

def download_directory_files(file_list, source_dir, target_dir):
    for filename in file_list:
        source_path = f"{source_dir}/{filename}"
        target_path = os.path.join(target_dir, filename)
        url = get_github_raw_url(source_path)
        download_file(url, target_path)

def download_steam_file():
    url = get_github_raw_url(STEAM_FILE["source"])
    if not is_admin():
        return False
    return download_file(url, STEAM_FILE["target"])

def main():
    username = os.getlogin()
    target_base_dir = Path(f"C:/Users/{username}/Saved Games/Respawn/Apex")

    print("AUTO APEX SETTINGS")
    print("=" * 50)
    print(Fore.GREEN + f"user detect: {username}" + Style.RESET_ALL)
    print(f"succes (user): {target_base_dir}")
    print(f"succes (Steam): {STEAM_FILE['target']}")
    print("=" * 50)

    os.makedirs(target_base_dir, exist_ok=True)

    download_directory_files(LOCAL_FILES, "local", target_base_dir / "local")
    download_directory_files(PROFILE_FILES, "profile", target_base_dir / "profile")
    steam_success = download_steam_file()

    print("\nlocal :")
    for file in (target_base_dir / "local").glob('*'):
        print(f"  - {file.name}")

    print("\nprofile :")
    for file in (target_base_dir / "profile").glob('*'):
        print(f"  - {file.name}")

    print("\nSteam :")
    print(f"  - autoexec.cfg -> {STEAM_FILE['target']}")
    print(Fore.GREEN + "\nOPERATION TERMINEE" + Style.RESET_ALL)

    print(Fore.YELLOW + "\nL'auto-close in 10 secondes..." + Style.RESET_ALL)
    time.sleep(10)

if __name__ == "__main__":
    main()

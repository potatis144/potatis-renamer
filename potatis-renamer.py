import os
import re
from datetime import datetime
import time
import sys

ascii_header = r"""
               __          __  .__                                                                    
______   _____/  |______ _/  |_|__| ______         _______   ____   ____ _____    _____   ___________ 
\____ \ /  _ \   __\__  \\   __\  |/  ___/  ______ \_  __ \_/ __ \ /    \\__  \  /     \_/ __ \_  __ \
|  |_> >  <_> )  |  / __ \|  | |  |\___ \  /_____/  |  | \/\  ___/|   |  \/ __ \|  Y Y  \  ___/|  | \/
|   __/ \____/|__| (____  /__| |__/____  >          |__|    \___  >___|  (____  /__|_|  /\___  >__|   
|__|                    \/             \/                       \/     \/     \/      \/      \/       
"""

def clean_name(name):
    filler_match = re.search(r'(\[Filler\])', name, re.IGNORECASE)
    filler_tag = filler_match.group(1) if filler_match else ''
    name = re.sub(r'\[Filler\]', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\[.*?\]', '', name)
    name = re.sub(r'\(\d{4}\)', '', name)
    name = re.sub(r'\(.*?\)', '', name)
    name = re.sub(r'S\d{1,3}E\d{1,3}', '', name, flags=re.IGNORECASE)
    name = re.sub(r'[-_.]', ' ', name)
    name = re.sub(r'\s+', ' ', name)
    name = name.strip().strip('-')
    return f"{name} {filler_tag}".strip()

def suggest_show_name(folder, files):
    folder_name = os.path.basename(os.path.dirname(folder))
    folder_clean = clean_name(folder_name).lower()
    name_scores = {}
    for file in files:
        base = os.path.splitext(file)[0]
        cleaned = clean_name(base).lower()
        if folder_clean in cleaned:
            return folder_clean.title()
        words = cleaned.split()
        for i in range(len(words)):
            guess = ' '.join(words[i:i+len(folder_clean.split())])
            if guess:
                name_scores[guess] = name_scores.get(guess, 0) + 1
    best_guess = max(name_scores, key=name_scores.get, default=folder_clean)
    return best_guess.title()

def extract_episode_number(filename):
    patterns = [
        r'[Ss](\d+)[Ee](\d+)',
        r'Season\s*(\d+)[^\d]*(\d+)',
        r'[\s_](\d{1,3})[\s_.]',
        r'[Ee]p?\s?(\d+)',
        r'\b(\d{1,3})\b'
    ]
    for pattern in patterns:
        match = re.search(pattern, filename, re.IGNORECASE)
        if match:
            if len(match.groups()) == 2:
                return match.group(1).zfill(2), match.group(2).zfill(2)
            else:
                return None, match.group(1).zfill(2)
    return None, None

def rename_files():
    os.system("cls" if os.name == "nt" else "clear")
    print(ascii_header)

    folder = input("📂 Enter folder path: ").strip('"')
    if not os.path.isdir(folder):
        print("❌ Error: Folder does not exist.")
        return

    files = [f for f in os.listdir(folder) if f.lower().endswith((".mkv", ".mp4", ".avi"))]
    files.sort()

    if not files:
        print("⚠️ No video files found in the folder.")
        return

    default_show_name = suggest_show_name(folder, files)
    show_name = input(f"🎬 Enter show name (Suggested: {default_show_name}): ").strip() or default_show_name
    season_input = input(f"📅 Enter season number (Suggested: 1): ").strip()
    season_number = season_input if season_input else "1"
    force_renumber = input("📺 Start episode numbering from 1 instead of file name? (Y/N): ").strip().lower() == 'y'

    log_path = os.path.join(folder, "rename-log.txt")
    log_entries = []
    divider = "─" * 50
    timestamp_now = datetime.now().strftime("%Y-%m-%d %H:%M")

    if not os.path.exists(log_path) or os.stat(log_path).st_size == 0:
        log_entries.append(f"{ascii_header}\n")

    log_entries.append(f"{divider}")
    log_entries.append(f"🎥 🕒 Run at: {timestamp_now}")
    log_entries.append(f"{divider}")

    preview_changes = []
    episode_counter = 1

    for file in files:
        ext = os.path.splitext(file)[1]
        season, episode = extract_episode_number(file)

        if not force_renumber and not episode:
            continue

        season_str = season.zfill(2) if season else season_number.zfill(2)

        if force_renumber:
            episode_str = str(episode_counter).zfill(2)
            episode_counter += 1
        else:
            episode_str = episode.zfill(2)

        new_filename = f"{show_name} - S{season_str}E{episode_str}{ext}"
        preview_changes.append((file, new_filename))

    if not preview_changes:
        print("⚠️ No matching filenames found. Check your file formats.")
        return

    print("\n📌 Proposed changes:")
    for old, new in preview_changes:
        print(f"🔄 {old} ➡️ {new}")

    confirm = input("\n✅ Proceed with renaming? (Y/N): ").strip().lower()
    if confirm != 'y':
        print("❌ Operation cancelled.")
        return

    rename_start_time = time.time()
    for old, new in preview_changes:
        full_path = os.path.join(folder, old)
        new_path = os.path.join(folder, new)
        try:
            os.rename(full_path, new_path)
            log_entries.append(f"[{timestamp_now}] ✅ {old} -> {new}")
            print(f"✅ {old} -> {new}")
        except Exception as e:
            log_entries.append(f"[{timestamp_now}] ❌ Failed to rename {old}: {e}")
            print(f"❌ Failed to rename {old}: {e}")

    rename_duration = time.time() - rename_start_time
    log_entries.append(f"{divider}")
    log_entries.append(f"⏳ Rename Time: {rename_duration:.2f} seconds")
    log_entries.append(f"{divider}")

    with open(log_path, "a", encoding="utf-8") as log_file:
        for entry in log_entries:
            log_file.write(entry + "\n")

    print(f"\n📜 Log saved to: {log_path}")
    print(f"⏱️ Rename Time: {rename_duration:.2f} seconds")

if __name__ == "__main__":
    while True:
        rename_files()
        print("\n🔄 Press Enter to restart script, or Esc to exit.")
        if os.name == "nt":
            import msvcrt
            while True:
                key = msvcrt.getch()
                if key == b'\r':
                    break
                elif key == b'\x1b':
                    print("🚪 Exiting script...")
                    sys.exit()
        else:
            try:
                input("(Press Enter to continue, Ctrl+C to quit)")
            except KeyboardInterrupt:
                print("\n🚪 Exiting script...")
                sys.exit()

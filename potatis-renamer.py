import os
import re
from datetime import datetime
import time

# ASCII Art Header for Log
ascii_header = r"""
               __          __  .__                                                                    
______   _____/  |______ _/  |_|__| ______         _______   ____   ____ _____    _____   ___________ 
\____ \ /  _ \   __\__  \\   __\  |/  ___/  ______ \_  __ \_/ __ \ /    \\__  \  /     \_/ __ \_  __ \
|  |_> >  <_> )  |  / __ \|  | |  |\___ \  /_____/  |  | \/\  ___/|   |  \/ __ \|  Y Y  \  ___/|  | \/
|   __/ \____/|__| (____  /__| |__/____  >          |__|    \___  >___|  (____  /__|_|  /\___  >__|   
|__|                    \/             \/                       \/     \/     \/      \/     \/       
"""

# Display ASCII Art in Console
print(ascii_header)

# Inputs
folder = input("📂 Enter folder path: ").strip('"')
show_name = input("🎬 Enter show name: ").strip()
season_number = input("📅 Enter season number: ").zfill(2)

if not os.path.isdir(folder):
    print("❌ Error: Folder does not exist.")
    exit()

start_time = time.time()

log_path = os.path.join(folder, "rename-log.txt")
log_entries = []

divider = "─" * 50
timestamp_now = datetime.now().strftime("%Y-%m-%d %H:%M")

# If log file doesn't exist or is empty, write the ASCII header once
if not os.path.exists(log_path) or os.stat(log_path).st_size == 0:
    log_entries.append(f"{ascii_header}\n")

# Log header for this run
log_entries.append(f"{divider}")
log_entries.append(f"🎥 🕒 Run at: {timestamp_now}")
log_entries.append(f"{divider}")

files = [f for f in os.listdir(folder) if f.lower().endswith((".mkv", ".mp4", ".avi"))]
files.sort()

# Extract episode numbers while preserving original formatting
preview_changes = []

for file in files:
    ext = os.path.splitext(file)[1]

    # Extract episode numbers from filenames
    match = re.search(r"(?:S\d+E)?(\d+\.\d+|\d+)", file)
    if match:
        ep_num = match.group(1)

        # Ensure proper formatting for decimal episodes (E2.5 → E02.5)
        if "." in ep_num:
            int_part, dec_part = ep_num.split(".")
            formatted_ep = f"{int_part.zfill(2)}.{dec_part}"  # Ensure two-digit padding
        else:
            formatted_ep = ep_num.zfill(2)

        new_filename = f"{show_name} - S{season_number}E{formatted_ep}{ext}"
        preview_changes.append((file, new_filename))

# Preview changes
print("\n📌 Proposed changes:")
for old, new in preview_changes:
    print(f"🔄 {old} ➡️ {new}")

confirm = input("\n✅ Proceed with renaming? (Y/N): ").strip().lower()

if confirm != 'y':
    print("❌ Operation cancelled.")
    exit()

# Apply renaming
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

end_time = time.time()
duration = end_time - start_time
duration_str = f"{duration:.2f} seconds"

# Log footer
log_entries.append(f"{divider}")
log_entries.append(f"⏳ End of run (Duration: {duration_str})")
log_entries.append(f"{divider}")

# Append logs to the file, ensuring ASCII header stays at the top
with open(log_path, "a", encoding="utf-8") as log_file:
    for entry in log_entries:
        log_file.write(entry + "\n")

print(f"\n📜 Log saved to: {log_path}")
print(f"⏱️ Run time: {duration_str}")
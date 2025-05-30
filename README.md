# 📂 Potatis Renamer

**Potatis Renamer** is a powerful **Jellyfin-compatible episode renamer** that helps organize TV show files into a structured naming format.  
It ensures correct episode numbering, provides a preview before renaming, and logs all operations for easy tracking.

## 🚀 Features
✅ **Jellyfin-Friendly Naming** – Uses a standardized format for seamless indexing.  
✅ **Name suggestion** – It will try to suggest a name for the show.  
✅ **Smart Episode Detection** – Extracts episode numbers while preserving formatting.  
✅ **Preview Before Renaming** – See proposed changes before proceeding.  
✅ **Automatic Logging** – Creates `rename-log.txt` for tracking renaming attempts.  

## 🛠️ Installation & Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/potatis144/potatis-renamer.git
Navigate to the script folder:

bash
cd potatis-renamer
Run the script:

bash
python potatis-renamer.py
📖 Example Usage
📂 Enter folder path: "D:/TV Shows/Breaking Bad/Season 2"
🎬 Enter show name: Breaking Bad
📅 Enter season number: 2
🔄 The script renames files like:

Breaking Bad - S02E01.mkv
Breaking Bad - S02E02.mkv
Breaking Bad - S02E03.mkv
...
📜 Logging System
The script maintains a rename log (rename-log.txt), recording: ✔️ Successful renames ✅ ❌ Failed renames with error messages

🔧 Requirements
Python 3.x

os, re, datetime, time (built-in libraries)

📜 License
This project is open-source under the MIT License.

🤝 Contributions
Want to improve this script? Feel free to submit pull requests or report issues! 🚀

<video src="https://r2.e-z.host/90e02276-aaf6-441f-880e-09ebaabd2e85/268mzh2m.mkv" controls>
  Your browser does not support the video tag.
</video>

![Alt text](https://r2.e-z.host/90e02276-aaf6-441f-880e-09ebaabd2e85/2kj9lnoz.png)
![Alt text](https://r2.e-z.host/90e02276-aaf6-441f-880e-09ebaabd2e85/ai93agcz.png)

# HabitCalendar 

A minimalist desktop calendar app for tracking daily habits — built with Python and CustomTkinter.

![HabitCalendar](icon.png)

---

## ✨ Features

**Habit Tracking**
- Create multiple trackers, each with its own calendar and color
- Mark days with a single click — unmark by clicking again
- Navigate between months and years freely
- Each tracker stores its own history across multiple years

**Customization**
- 8 app color themes — from pink to purple to green
- Light and dark mode
- 9 languages: English, Portuguese, Spanish, French, Italian, Russian, Greek, Chinese, Korean

**Data & Backup**
- Internal backup with one click — restore to any previous save point
- Export your database to any folder for external backup
- Import a backup file from anywhere to restore your data
- All data stored locally — no accounts, no cloud, no tracking

**App**
- Remembers window size and maximized state between sessions
- Collapsible sidebar
- Runs as a native desktop app on Linux, Windows, and macOS

---

## 🚀 Getting Started

Download the latest release from the [Releases](../../releases) page.

### 🐧 Linux

**Option 1 — .deb package (Ubuntu, Debian, Pop!_OS)**

Download `habitcalendar_x.x.x_amd64.deb` and install:

```bash
sudo dpkg -i habitcalendar_*.deb
```

Or double-click the file in your file manager.

**Option 2 — Standalone executable (any distro)**

Download `HabitCalendar-linux`, mark as executable and run:

```bash
chmod +x HabitCalendar-linux
./HabitCalendar-linux
```

### 🪟 Windows

Download `HabitCalendar-windows.exe` and run it. No installation required.

### 🍎 macOS

Download `HabitCalendar-macos`. On first launch, macOS will block it because the app is not signed with an Apple Developer certificate. To run it:

```bash
xattr -cr HabitCalendar-macos
chmod +x HabitCalendar-macos
./HabitCalendar-macos
```

Or right-click the file → **Open** → **Open Anyway**.

This is a one-time step. The app is open source — you can verify the code yourself.

---

### Run from source

**Requirements:** Python 3.11+

```bash
git clone https://github.com/arthurkitice/HabitCalendar.git
cd HabitCalendar
python3 -m venv .venv
source .venv/bin/activate       # Linux/macOS
# .venv\Scripts\activate        # Windows
pip install -r requirements.txt
python main.py
```

### Build the executable yourself

```bash
./build.sh
# Output: dist/HabitCalendar
```

---

## 🗂 Data Location

All data is stored locally at:

**Linux/macOS**
```
~/.local/share/HabitCalendar/
├── database.db          # Your habit data
├── database.habitbackup # Internal backup
└── app_settings.json    # App preferences
```

**Windows**
```
C:\Users\<you>\AppData\Local\HabitCalendar\
├── database.db
├── database.habitbackup
└── app_settings.json
```

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11+ |
| GUI | CustomTkinter |
| Database | SQLite via SQLAlchemy |
| Icons | CairoSVG + Pillow |
| i18n | python-i18n |
| Packaging | PyInstaller |

**Architecture:** Repository Pattern with DTOs for clean separation between data and UI layers.

---

## 🌍 Supported Languages

| Code | Language |
|---|---|
| `en` | English |
| `pt` | Português |
| `es` | Español |
| `fr` | Français |
| `it` | Italiano |
| `ru` | Русский |
| `el` | Ελληνικά |
| `zh` | 中文 |
| `ko` | 한국어 |

Language is detected automatically from the system on first launch and can be changed anytime in settings.

---

## 📄 License

MIT License — do whatever you want with it.

## 📄 Credits

Icons by [Lucide](https://lucide.dev) — ISC License.

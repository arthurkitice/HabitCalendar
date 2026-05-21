#!/bin/bash
# Script para compilar o executável do HabitCalendar usando PyInstaller
source .venv/bin/activate
pyinstaller --onefile --windowed \
  --name "HabitCalendar" \
  --icon "icon.png" \
  --add-data "locales:locales" \
  --add-data "ui/icons:ui/icons" \
  --add-data "icon.png:." \
  --hidden-import "PIL._tkinter_finder" \
  --hidden-import "PIL._imagingtk" \
  main.py
echo "Build concluído: dist/HabitCalendar"
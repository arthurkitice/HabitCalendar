#!/bin/bash
# Script para compilar o executável do HabitCalendar usando PyInstaller
source .venv/bin/activate
pyinstaller --onefile --windowed --strip --optimize 2 \
  --name "HabitCalendar" \
  --icon "icon.png" \
  --add-data "locales:locales" \
  --add-data "ui/icons:ui/icons" \
  --add-data "icon.png:." \
  --hidden-import "PIL._tkinter_finder" \
  --hidden-import "PIL._imagingtk" \
  --exclude-module "greenlet" \
  --exclude-module "sqlalchemy.dialects.postgresql" \
  --exclude-module "sqlalchemy.dialects.mysql" \
  --exclude-module "sqlalchemy.dialects.oracle" \
  --exclude-module "sqlalchemy.dialects.mssql" \
  --exclude-module "sqlalchemy.testing" \
  --exclude-module "tkinter.test" \
  --exclude-module "sqlite3.test" \
  --exclude-module "test" \
  --exclude-module "pydoc" \
  --exclude-module "bdb" \
  --exclude-module "pdb" \
  --exclude-module "xmlrpc" \
  --exclude-module "http.server" \
  main.py
echo "Build concluído: dist/HabitCalendar"
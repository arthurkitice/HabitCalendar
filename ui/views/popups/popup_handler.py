from .alter_tracker_view import AlterTrackerFrame
from .new_year_view import NewYearView
from .tracker_view import TrackerFrame
from .year_view import YearView
from .theme_view import ThemeView
from .settings_view import SettingsView
from .backup_view import BackupView
from .confirmation_view import ConfirmationView
import i18n

def alter_tracker_popup(parent, on_save, tracker_name=None, tracker_id=None):
    return AlterTrackerFrame(parent.winfo_toplevel(), on_save, tracker_name, tracker_id)

def delete_tracker_popup(parent, on_save, tracker_name):
    label = i18n.t('delete.tracker.label', tracker=tracker_name)
    message = i18n.t('delete.tracker.warning')
    return ConfirmationView(parent.winfo_toplevel(), on_save, label, message)

def delete_year_popup(parent, on_save, year):
    label = i18n.t('delete.year.label', year=year)
    message = i18n.t('delete.year.warning')
    return ConfirmationView(parent.winfo_toplevel(), on_save, label, message)

def new_year_popup(parent, on_save, year):
    label = i18n.t('new_year.label', year=year)
    message = i18n.t('new_year.warning')
    return NewYearView(parent.winfo_toplevel(), on_save, label, message)

def save_backup_popup(parent, on_save):
    label = i18n.t('save_backup.label')
    message = i18n.t('save_backup.message')
    return ConfirmationView(parent.winfo_toplevel(), on_save, label, message)

def restore_backup_popup(parent, on_save):
    label = i18n.t('restore_backup.label')
    message = i18n.t('restore_backup.message')
    return ConfirmationView(parent.winfo_toplevel(), on_save, label, message)

def import_popup(parent, on_save):
    label = i18n.t('import_backup.label')
    message = i18n.t('import_backup.message')
    return ConfirmationView(parent.winfo_toplevel(), on_save, label, message)

def tracker_popup(parent, tracker_name, tracker_id, on_year_remove):
    return TrackerFrame(parent.winfo_toplevel(), tracker_id, tracker_name, on_year_remove)

def year_popup(parent, on_select, tracker_id, year, on_new_year):
    return YearView(parent.winfo_toplevel(), tracker_id, on_select, year, on_new_year)

def theme_popup(parent, on_color_change, on_theme_change):
    return ThemeView(parent.winfo_toplevel(), on_color_change, on_theme_change)

def settings_popup(parent, on_color_change, on_theme_change, on_language_change, on_restore_backup):
    return SettingsView(parent.winfo_toplevel(), on_color_change, on_theme_change, on_language_change, on_restore_backup)

def backup_popup(parent, on_restore_backup):
    return BackupView(parent.winfo_toplevel(), on_restore_backup)

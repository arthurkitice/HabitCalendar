import shutil, os, logging, sqlite3
from contextlib import closing
from database import APP_DIR, close_global_connection

BACKUP_PATH = os.path.join(APP_DIR, 'database.habitbackup')
DB_PATH = os.path.join(APP_DIR, 'database.db')
REQUIRED_TABLES = {'trackers', 'years', 'months', 'days'}

PRE_RESTORE_PATH = os.path.join(APP_DIR, 'pre_restore.habitbackup')
PRE_IMPORT_PATH = os.path.join(APP_DIR, 'pre_import.habitbackup')

def create_backup() -> bool:
    try:
        # O 'closing' garante o fechamento absoluto e limpa o -wal imediatamente
        with closing(sqlite3.connect(DB_PATH)) as source:
            with closing(sqlite3.connect(BACKUP_PATH)) as dest:
                source.backup(dest)
                
        logging.getLogger(__name__).info(f"Backup criado com segurança em {BACKUP_PATH}")
        return True
    except Exception as e:
        logging.getLogger(__name__).error(f"Erro ao criar backup: {e}", exc_info=True)
        return False

def validate_backup(path: str) -> bool:
    try:
        with closing(sqlite3.connect(path)) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = {row[0] for row in cursor.fetchall()}
            return REQUIRED_TABLES.issubset(tables)
            
    except Exception as e:
        logging.getLogger(__name__).error(f"Erro ao validar backup em {path}: {e}")
        return False

def restore_backup() -> bool:
    try:
        if not os.path.exists(BACKUP_PATH):
            return False
        if not validate_backup(BACKUP_PATH):
            return False
            
        close_global_connection()
        
        shutil.copy2(DB_PATH, PRE_RESTORE_PATH)
        
        with closing(sqlite3.connect(BACKUP_PATH)) as source:
            with closing(sqlite3.connect(DB_PATH)) as dest:
                source.backup(dest)
                
        logging.getLogger(__name__).info("Backup restaurado com sucesso")
        return True
    except Exception as e:
        logging.getLogger(__name__).error(f"Erro ao restaurar backup: {e}", exc_info=True)
        return False

def export_database(destination_path: str) -> bool:
    try:
        with closing(sqlite3.connect(DB_PATH)) as source:
            with closing(sqlite3.connect(destination_path)) as dest:
                source.backup(dest)
                
        logging.getLogger(__name__).info(f"Dados exportados com sucesso para {destination_path}")
        return True
    except Exception as e:
        logging.getLogger(__name__).error(f"Erro ao exportar: {e}", exc_info=True)
        return False

def import_database(external_path: str) -> bool:
    try:
        if not os.path.exists(external_path):
            return False
            
        if not validate_backup(external_path):
            logging.getLogger(__name__).warning("Tentativa de importar um arquivo inválido.")
            return False
            
        close_global_connection()
        
        shutil.copy2(DB_PATH, PRE_IMPORT_PATH)
        
        with closing(sqlite3.connect(external_path)) as source:
            with closing(sqlite3.connect(DB_PATH)) as dest:
                source.backup(dest)
                
        logging.getLogger(__name__).info(f"Backup importado com sucesso de: {external_path}")
        return True
        
    except Exception as e:
        logging.getLogger(__name__).error(f"Erro ao importar backup externo: {e}", exc_info=True)
        return False

def get_backup_info() -> float | None:
    """Retorna o timestamp bruto de modificação do arquivo."""
    if not os.path.exists(BACKUP_PATH):
        return None
    return os.path.getmtime(BACKUP_PATH)
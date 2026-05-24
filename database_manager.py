import shutil, os, logging, datetime, sqlite3
from database import APP_DIR

BACKUP_PATH = os.path.join(APP_DIR, 'database.habitbackup')
DB_PATH = os.path.join(APP_DIR, 'database.db')
REQUIRED_TABLES = {'trackers', 'years', 'months', 'days'}

def create_backup() -> bool:
    try:
        with sqlite3.connect(DB_PATH) as source:
            with sqlite3.connect(BACKUP_PATH) as dest:
                source.backup(dest)
                
        logging.getLogger(__name__).info(f"Backup criado com segurança em {BACKUP_PATH}")
        return True
    except Exception as e:
        logging.getLogger(__name__).error(f"Erro ao criar backup: {e}", exc_info=True)
        return False

def validate_backup(path: str) -> bool:
    try:
        from sqlalchemy import create_engine, inspect
        engine = create_engine(f"sqlite:///{path}")
        tables = set(inspect(engine).get_table_names())
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
        shutil.copy2(DB_PATH, DB_PATH + '.pre_restore')
        shutil.copy2(BACKUP_PATH, DB_PATH)
        logging.getLogger(__name__).info("Backup restaurado com sucesso")
        return True
    except Exception as e:
        logging.getLogger(__name__).error(f"Erro ao restaurar backup: {e}", exc_info=True)
        return False

def export_database(destination_path: str) -> bool:
    try:
        # Pega o banco atual (vivo) e faz uma cópia limpa para o local escolhido
        with sqlite3.connect(DB_PATH) as source:
            with sqlite3.connect(destination_path) as dest:
                source.backup(dest)
                
        logging.getLogger(__name__).info(f"Dados exportados com sucesso para {destination_path}")
        return True
    except Exception as e:
        logging.getLogger(__name__).error(f"Erro ao exportar: {e}", exc_info=True)
        return False

def import_database(external_path: str) -> bool:
    """
    Importa um backup externo e substitui o banco de dados atual,
    criando um arquivo de segurança antes da substituição.
    """
    try:
        # 1. Verifica se o arquivo realmente existe
        if not os.path.exists(external_path):
            return False
            
        # 2. Valida se o arquivo escolhido tem a estrutura correta do HabitCalendar
        if not validate_backup(external_path):
            logging.getLogger(__name__).warning("Tentativa de importar um arquivo que não é um banco de dados válido.")
            return False
            
        # 3. Cria a rede de segurança (salva como estava antes do usuário fazer besteira)
        shutil.copy2(DB_PATH, DB_PATH + '.pre_import')
        
        # 4. Faz a injeção dos dados novos de forma segura (sem dar erro de arquivo em uso)
        with sqlite3.connect(external_path) as source:
            with sqlite3.connect(DB_PATH) as dest:
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
import pyodbc
import os
from datetime import datetime
import time

# Configurações de conexão ao SQL Server
server = os.getenv('SQL_SERVER', 'servidor')
database = os.getenv('SQL_DATABASE', 'nome do banco')
username = os.getenv('SQL_USERNAME', 'nome de usuario')
password = os.getenv('SQL_PASSWORD', 'senha')
driver = os.getenv('SQL_DRIVER', '{ODBC Driver 17 for SQL Server}')

# Diretório onde você deseja salvar o backup
backup_directory = 'C:\\Program Files\\Microsoft SQL Server\\MSSQL15.MSSQLSERVER\\MSSQL\\Backup'

def generate_backup_filename(database):
    # Gera o nome do arquivo de backup com timestamp
    return f'{database}_backup_{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.bak'

def create_backup_query(database, backup_path):
    # Cria a consulta SQL para realizar o backup
    return f"""
    BACKUP DATABASE {database} 
    TO DISK = N'{backup_path}' 
    WITH NOFORMAT, NOINIT, 
    NAME = N'{database}-Full Database Backup', 
    SKIP, NOREWIND, NOUNLOAD, STATS = 10
    """

def check_backup_query():
    # Consulta SQL para verificar se o backup foi concluído com sucesso
    return """
    SELECT
        A.database_name AS [Database Name],
        A.backup_start_date AS [Backup Start Date],
        A.backup_finish_date AS [Backup Finish Date],
        CASE A.type
            WHEN 'D' THEN 'Full'
            WHEN 'I' THEN 'Differential'
            WHEN 'L' THEN 'Transaction Log'
            WHEN 'F' THEN 'File/Filegroup'
            WHEN 'G' THEN 'Differential File'
            WHEN 'P' THEN 'Partial'
            WHEN 'Q' THEN 'Differential partial'
        END AS [Backup Type],
        B.physical_device_name AS [Backup Location],
        A.backup_size AS [Backup Size]
    FROM
        msdb.dbo.backupset A
    INNER JOIN msdb.dbo.backupmediafamily B ON A.media_set_id = B.media_set_id
    WHERE
        A.database_name = ? 
        AND A.backup_finish_date = (
            SELECT
                MAX(backup_finish_date)
            FROM
                msdb.dbo.backupset
            WHERE
                database_name = ? 
                AND type = 'D'
        );
    """

def perform_backup():
    backup_filename = generate_backup_filename(database)
    backup_path = os.path.join(backup_directory, backup_filename)
    backup_query = create_backup_query(database, backup_path)

    try:
        # Conecta ao SQL Server
        conn = pyodbc.connect(
            f'SERVER={server};DATABASE={database};UID={username};PWD={password};DRIVER={driver}')
        conn.autocommit = True
        cursor = conn.cursor()

        # Executa o comando de backup
        cursor.execute(backup_query)
        print(f'Backup do banco de dados {database} iniciado. Caminho do backup: {backup_path}')

        # Verifica se o backup foi concluído com sucesso
        while True:
            cursor.execute(check_backup_query(), (database, database))
            row = cursor.fetchone()
            if row:
                print('Backup concluído com sucesso!')
                print('Detalhes do Backup:')
                print(f'Nome do Banco de Dados: {row[0]}')
                print(f'Data e Hora de Início do Backup: {row[1]}')
                print(f'Data e Hora de Conclusão do Backup: {row[2]}')
                print(f'Tipo de Backup: {row[3]}')
                print(f'Localização do Backup: {row[4]}')
                print(f'Tamanho do Backup: {row[5]}')
                break
            else:
                print('Aguardando conclusão do backup...')
                time.sleep(10)  # Verifica a cada 10 segundos se o backup foi concluído

    except pyodbc.Error as e:
        print(f'Erro ao realizar o backup: {e}')

    except Exception as e:
        print(f'Erro inesperado: {e}')

    finally:
        # Fecha a conexão
        if 'conn' in locals() and conn is not None:
            conn.close()

if __name__ == '__main__':
    perform_backup()

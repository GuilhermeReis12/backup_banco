# Backup de Banco de Dados SQL Server com Python

Este projeto em Python realiza backups automatizados de um banco de dados SQL Server, salvando os arquivos de backup em um diretório especificado. Ele inclui verificações para garantir que o backup foi concluído com sucesso.

## Funcionalidades

- Realiza backup completo de um banco de dados SQL Server.
- Gera nome do arquivo de backup com timestamp.
- Verifica se o backup foi concluído com sucesso e exibe detalhes do backup.
- Utiliza variáveis de ambiente para armazenar informações sensíveis.

## Tecnologias Utilizadas

- **Python**: Linguagem de programação utilizada.
- **pyodbc**: Biblioteca Python para acessar bancos de dados ODBC.
- **ODBC Driver 17 for SQL Server**: Driver ODBC para conectar ao SQL Server.

## Como Executar

### Pré-requisitos

1. **Python 3.6+**: Certifique-se de ter o Python instalado na sua máquina.
2. **Pacote pyodbc**: Você pode instalá-lo usando o pip.
    ```sh
    pip install pyodbc
    ```
3. **Driver ODBC para SQL Server**: Instale o ODBC Driver 17 for SQL Server. [Instruções de instalação](https://docs.microsoft.com/pt-br/sql/connect/odbc/download-odbc-driver-for-sql-server).

### Configuração

Crie um arquivo `.env` na raiz do projeto para definir as variáveis de ambiente necessárias:
```env
SQL_SERVER=servidor
SQL_DATABASE=nome_do_banco
SQL_USERNAME=nome_de_usuario
SQL_PASSWORD=senha
SQL_DRIVER={ODBC Driver 17 for SQL Server}

<!-- pode configurar o drive para o 17 ou 18  -->

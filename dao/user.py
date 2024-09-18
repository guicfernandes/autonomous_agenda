from entities.user import User
from utils.connection import start_connection, get_cursor, close_connection


def create_table() -> None:
    """Function the create Clientes table
    """
    conn = start_connection()
    cursor = get_cursor(connection=conn)
    # Criar a tabela de agendamentos se ainda nao existe
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS clientes
        (cliente_id INTEGER PRIMARY KEY, nome TEXT, email TEXT)
        '''
    )
    conn.commit()
    close_connection(connection=conn)


def get_user(user_id:int = None, user_name: str = None, user_email: str = None) -> User:
    """Function to get User object from database.
    If user_id is provided, we don't need user_name and user_email.
    Else, we need both user_name and user_email.

    Args:
        user_id (int, optional): User id. Defaults to None.
        user_name (str, optional): User name. Defaults to None.
        user_email (str, optional): User email. Defaults to None.

    Returns:
        User: User object
    """
    conn = start_connection()
    cursor = get_cursor(connection=conn)
    filter_id = True if user_id else False
    if filter_id:
        row = cursor.execute(
            "SELECT * FROM clientes WHERE cliente_id = ? LIMIT 1",
            user_id
        )
    else:
        row = cursor.execute(
            "SELECT * FROM clientes WHERE nome = ? AND email = ?",
            user_name, user_email
        )
    close_connection(connection=conn)
    user = User(id=row[0], name=row[1], email=row[2])
    return user

def add_user(name: str, email: str) -> None:
    """Function to add a client User to the database

    Args:
        name (str): User name
        email (str): User email
    """
    conn = start_connection()
    cursor = get_cursor(connection=conn)
    cursor.execute(
        "INSERT INTO clientes (cliente_id, nome, email) VALUES (?, ?, ?)",
        (name, email) 
    )
    conn.commit()
    close_connection(connection=conn)
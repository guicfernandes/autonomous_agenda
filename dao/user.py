"""Module to handle User client data access object (DAO) operations"""

from entities.user import User
from connection.db_connection import start_connection, get_cursor, close_connection
from utils.exceptions import UserNotFoundException


def create_table_user() -> None:
    """Function the create Clientes table"""
    conn = start_connection()
    cursor = get_cursor(connection=conn)
    # Criar a tabela de agendamentos se ainda nao existe
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS clientes
        (cliente_id INTEGER PRIMARY KEY, nome TEXT, email TEXT)
        """
    )
    conn.commit()
    close_connection(connection=conn)


def list_users() -> list:
    """Function to list all users from database

    Returns:
        list: List of User objects
    """
    conn = start_connection()
    cursor = get_cursor(connection=conn)
    cursor.execute("SELECT * FROM clientes")
    rows = cursor.fetchall()
    close_connection(connection=conn)
    users = []
    for row in rows:
        user = User(id=row[0], name=row[1], email=row[2])
        users.append(user)
    return users


# TODO: delete this function and replace for a new one "get_user_by_id"
def get_user(
    user_id: int = None, user_name: str = None, user_email: str = None
) -> User:
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
        cursor.execute("SELECT * FROM clientes WHERE cliente_id = ?", (str(user_id),))
    else:
        cursor.execute(
            "SELECT * FROM clientes WHERE nome = ? AND email = ? LIMIT 1",
            (
                user_name,
                user_email,
            ),
        )
    row = cursor.fetchone()
    close_connection(connection=conn)
    if row:
        user = User(id=row[0], name=row[1], email=row[2])
    else:
        user = None
        raise UserNotFoundException(user_name=user_name, user_email=user_email)
    return user


def validate_if_user_already_exists(email: str) -> bool:
    """Function to validate if user already exists in the database

    Args:
        email (str): User email

    Returns:
        bool: True if user already exists, False otherwise
    """
    conn = start_connection()
    cursor = get_cursor(connection=conn)
    cursor.execute("SELECT * FROM clientes WHERE email = ?", (email,))
    row = cursor.fetchone()
    close_connection(connection=conn)
    if row:
        return True
    return False


def create_user(name: str, email: str) -> None:
    """Function to add a client User to the database

    Args:
        name (str): User name
        email (str): User email
    """
    conn = start_connection()
    cursor = get_cursor(connection=conn)
    cursor.execute("INSERT INTO clientes (nome, email) VALUES (?, ?)", (name, email))
    conn.commit()
    close_connection(connection=conn)


# TODO: replace "id" for "user_id"
def delete_user(name: str = None, email: str = None, id: int = None) -> None:
    """Function to delete User client

    Args:
        name (str): Client name
        email (str): Client email
        id (int): Client id. Defaults to None.
    """
    conn = start_connection()
    cursor = get_cursor(connection=conn)
    if not id:
        user = get_user(user_name=name, user_email=email)
    else:
        user = get_user(user_id=id)
    try:
        # user = get_user(user_name=name, user_email=email)
        cursor.execute(
            "DELETE FROM clientes WHERE cliente_id = ?", str(user.get_user_id())
        )
        conn.commit()
        print(
            f"Usuário {name} de e-mail {email} deletado com sucesso do banco de dados."
        )
    except UserNotFoundException as e:
        print(f"Erro ao deletar usuário:\n{e}")
    finally:
        close_connection(connection=conn)


# TODO: replace "id" for "user_id"
def update_user(
    name: str = None,
    current_email: str = None,
    id: int = None,
    new_name: str = None,
    new_email: str = None,
) -> None:
    """Function to update User client

    Args:
        name (str): Client name
        current_email (str): Client current email
        new_name (str, optional): New client name. Defaults to None.
        new_email (str, optional): New client email. Defaults to None.
    """
    conn = start_connection()
    cursor = get_cursor(connection=conn)
    try:
        if not id:
            user = get_user(user_name=name, user_email=current_email)
        else:
            user = get_user(user_id=id)
        if new_name:
            cursor.execute(
                "UPDATE clientes SET nome = ? WHERE cliente_id = ?",
                (new_name, str(user.get_user_id())),
            )
        if new_email:
            cursor.execute(
                "UPDATE clientes SET email = ? WHERE cliente_id = ?",
                (new_email, str(user.get_user_id())),
            )
        conn.commit()
        print(
            f"Usuário {name} de e-mail {current_email} atualizado com sucesso no banco de dados."
        )
    except UserNotFoundException as e:
        print(f"Erro ao atualizar usuário:\n{e}")
    finally:
        close_connection(connection=conn)
    return get_user(user_id=user.get_user_id())

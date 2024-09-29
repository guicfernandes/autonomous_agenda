"""Module to manage the Users data access object (DAO) operations"""

from entities.users import Users
from connection.db_connection import start_connection, get_cursor, close_connection
from utils.exceptions import UserNotFoundException


def create_table_users() -> None:
    """Function the create Users table"""
    conn = start_connection()
    cursor = get_cursor(connection=conn)
    # Create users table if not exists
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            password TEXT,
            birth_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    close_connection(connection=conn)


def create_user(
    first_name: str, last_name: str, email: str, password: str, birth_date: str
) -> None:
    """Function to create a new user

    Args:
        first_name (str): User first name
        last_name (str): User last name
        email (str): User email
        password (str): User password
        birth_date (str): User birth date
    """
    conn = start_connection()
    cursor = get_cursor(connection=conn)
    cursor.execute(
        """
        INSERT INTO users (first_name, last_name, email, password, birth_date, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """,
        (first_name, last_name, email, password, birth_date),
    )
    conn.commit()
    close_connection(connection=conn)


def delete_user(user_id: int) -> None:
    """Function to delete a user

    Args:
        user_id (int): User id
    """
    conn = start_connection()
    cursor = get_cursor(connection=conn)
    cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
    conn.commit()
    close_connection(connection=conn)


def update_user_email_and_password(user_id: int, email: str, password: str) -> None:
    """Function to update user email and password

    Args:
        user_id (int): User id
        email (str): User email
        password (str): User password
    """
    conn = start_connection()
    cursor = get_cursor(connection=conn)
    cursor.execute(
        "UPDATE users SET email = ?, password = ?, updated_at = CURRENT_TIMESTAMP WHERE user_id = ?",
        (email, password, user_id),
    )
    conn.commit()
    close_connection(connection=conn)


# TODO: implement update user object (first_name, last_name, birth_date, email, password)


def get_user_by_email(email: str) -> Users:
    """Function to get User object by email

    Args:
        email (str): User email

    Returns:
        Users: User object
    """
    conn = start_connection()
    cursor = get_cursor(connection=conn)
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    row = cursor.fetchone()
    close_connection(connection=conn)
    if row:
        user = Users(
            user_id=row[0],
            first_name=row[1],
            last_name=row[2],
            email=row[3],
            birth_date=row[5],
        )
        return user
    raise UserNotFoundException(user_email=email)


def get_user_by_id(user_id: int) -> Users:
    """Function to get User object by id

    Args:
        user_id (int): User id

    Returns:
        Users: User object
    """
    conn = start_connection()
    cursor = get_cursor(connection=conn)
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    close_connection(connection=conn)
    if row:
        user = Users(
            user_id=row[0],
            first_name=row[1],
            last_name=row[2],
            email=row[3],
            birth_date=row[5],
        )
        return user
    raise UserNotFoundException()


def get_all_users() -> list[Users]:
    """Function to get all users from the database

    Returns:
        list[Users]: List of Users objects
    """
    conn = start_connection()
    cursor = get_cursor(connection=conn)
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    close_connection(connection=conn)
    users = []
    for row in rows:
        user = Users(
            user_id=row[0],
            first_name=row[1],
            last_name=row[2],
            email=row[3],
            birth_date=row[5],
        )
        users.append(user)
    return users


def validate_if_user_already_exists(email: str) -> bool:
    """Function to validate if user already exists in the database

    Args:
        email (str): User email

    Returns:
        bool: True if user already exists, False otherwise
    """
    conn = start_connection()
    cursor = get_cursor(connection=conn)
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    row = cursor.fetchone()
    close_connection(connection=conn)
    if row:
        return True
    return False

""" Module to handle database connection """

from sqlite3 import connect
from sqlite3 import Connection, Cursor


def start_connection() -> Connection:
    """Function to start database connection

    Returns:
        Connection: Connection object to the database
    """
    conn = connect("agenda.db")
    return conn


def close_connection(connection: Connection) -> None:
    """Function to close connection to the database

    Args:
        connection (Connection): Connection to the database object
    """
    connection.close()


def get_cursor(connection: Connection) -> Cursor:
    """Function to get cursor connection

    Args:
        connection (Connection): Connection to the database object

    Returns:
        Cursor: Database cursor
    """
    return connection.cursor()

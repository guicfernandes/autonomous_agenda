from entities.user import User
from entities.agendamento import Appointment
from utils.connection import start_connection, get_cursor, close_connection
from dao.user import get_user
from datetime import datetime


def create_table() -> None:
    """Function to create agendamentos table
    """
    conn = start_connection()
    cursor = get_cursor(connection=conn)
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS agendamentos
        (agendamento_id INTEGER PRIMARY KEY, cliente_id INTEGER, data_agendamento TEXT, data_atualizacao TEXT
            CONSTRAINT fk_clientes
            FOREIGN KEY (cliente_id)
            REFERENCES clientes(cliente_id)
        )
        '''
    )
    conn.commit()
    close_connection(connection=conn)

def get_user_next_appointment(user: User) -> Appointment:
    """Function to get next appointment for a given client user.

    Args:
        user (User): Client we want to get next appointment

    Returns:
        Appointment: Next appointment for the given user
    """
    conn = start_connection()
    cursor = get_cursor(connection=conn)
    current_date = datetime.now()
    row = cursor.execute(
        "SELECT * FROM agendamentos WHERE cliente_id = ? AND data_agendamento > ? ORDER BY data_agendamento LIMIT 1", 
        (user.get_user_id(), current_date)
    )
    appointment = Appointment(id=row[0], user=user, date=row[2])
    close_connection(connection=conn)
    return appointment

def list_appointments(in_past: bool = False, in_future: bool = False, all: bool = True) -> list:
    """Function to get and list all appointments.
    We could fetch only past events, only future events or all events from the database using bool variables.

    Args:
        in_past (bool, optional): If we want to fetch only past events. Defaults to False.
        in_future (bool, optional): If we want to fetch only future events. Defaults to False.
        all (bool, optional): If we want to provide all events. Defaults to True.

    Returns:
        list: List of appointments fetched from database
    """
    conn = start_connection()
    cursor = get_cursor(connection=conn)
    current_date = datetime.now()
    if in_past:
        cursor.execute(
            "SELECT * FROM agendamentos WHERE data_agendamento < ?",
            current_date.strftime("%Y-%m-%d %H:%M")
        )
    elif in_future:
        cursor.execute(
            "SELECT * FROM agendamentos WHERE data_agendamento >= ?",
            current_date.strftime("%Y-%m-%d %H:%M")
        )
    else:
        cursor.execute("SELECT * FROM agendamentos")
    appointments = cursor.fetchall()
    close_connection(connection=conn)
    print(f"Lista de agendamentos: {appointments}")
    return appointments


def add_appointment(appointment_date: str, user: User) -> None:
    """Function to add an appointment to agenda

    Args:
        appointment_date (str): Appointment date
    """
    conn = start_connection()
    cursor = get_cursor(connection=conn)
    client_id = user.get_user_id()
    update_date = datetime.now()
    cursor.execute(
        "INSERT INTO agendamentos (cliente_id, data_agendamento, data_atualizacao) VALUES (?, ?, ?, ?)", 
        (client_id, appointment_date, update_date)
    )
    conn.commit()
    close_connection(connection=conn)
    print("Agendamento efetuado com sucesso")

from entities.user import User
from entities.agendamento import Appointment
from connection.db_connection import start_connection, get_cursor, close_connection
from utils.exceptions import AppointmentNotFoundException, UserNotFoundException, NoAppointmentsForSpecifiedPeriod
from dao.user import get_user
from datetime import datetime, timedelta


def create_table_appointment() -> None:
    """Function to create agendamentos table
    """
    conn = start_connection()
    cursor = get_cursor(connection=conn)
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS agendamentos(
            agendamento_id INTEGER PRIMARY KEY,
            cliente_id INTEGER,
            data_agendamento TEXT,
            data_atualizacao TEXT,
            CONSTRAINT fk_clientes
                FOREIGN KEY (cliente_id)
                REFERENCES clientes(cliente_id)
        )
        '''
    )
    conn.commit()
    close_connection(connection=conn)

def get_user_appointment(user: User, date: datetime = None) -> Appointment:
    """Function to get appointment for a given client user.
    Date could be provided to get appointment for a given date, but it should contain appointment's date and hour.
    If no date is provided, then the function returns the next appointment.

    Args:
        user (User): Client we want to get appointment
        date (datetime, optional): Date to get appointment. Defaults to None.

    Returns:
        Appointment: (Next) Appointment for the given user
    """
    conn = start_connection()
    cursor = get_cursor(connection=conn)
    if date:
        # Get appointment for a given date
        comparing_date = datetime.strptime(date, "%Y-%m-%d %H:%M")
        row = cursor.execute(
            "SELECT * FROM agendamentos WHERE cliente_id = ? AND data_agendamento = ? LIMIT 1", 
            (str(user.get_user_id()), comparing_date.strftime("%Y-%m-%d %H:%M"))
        ).fetchone()
    else:
        # Get next appointment
        comparing_date = datetime.now()
        row = cursor.execute(
            "SELECT * FROM agendamentos WHERE cliente_id = ? AND data_agendamento >= ? ORDER BY data_agendamento LIMIT 1", 
            (str(user.get_user_id()), comparing_date.strftime("%Y-%m-%d %H:%M"))
        ).fetchone()
    print(f"Row: {row}")
    close_connection(connection=conn)
    if row:
        appointment = Appointment(id=row[0], client=user, date=row[2])
    else:
        appointment = None
        raise AppointmentNotFoundException(user_name=user.get_user_name(), user_email=user.get_user_email(), date=comparing_date)        
    return appointment


def get_date_appointment(date: datetime) -> Appointment:
    """Function to get appointment for a given date.

    Args:
        date (datetime): Date to get appointment

    Returns:
        Appointment: Appointment for the given date
    """
    conn = start_connection()
    cursor = get_cursor(connection=conn)
    row = cursor.execute(
        "SELECT * FROM agendamentos WHERE data_agendamento = ? LIMIT 1", 
        (date.strftime("%Y-%m-%d %H:%M"),)
    ).fetchone()
    close_connection(connection=conn)
    if row:
        user = get_user(user_id=row[1])
        appointment = Appointment(id=row[0], client=user, date=row[2])
    else:
        appointment = None
        raise AppointmentNotFoundException(date=date)
    return appointment


def list_appointments(in_past: bool = False, in_future: bool = False, is_reminder: bool = False) -> list:
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
    reminder_date = current_date + timedelta(days=1)
    appointments = []
    if in_past:
        cursor.execute(
            "SELECT * FROM agendamentos WHERE data_agendamento < ?",
            (current_date.strftime("%Y-%m-%d %H:%M"),)
        )
    elif in_future:
        cursor.execute(
            "SELECT * FROM agendamentos WHERE data_agendamento >= ?",
            (current_date.strftime("%Y-%m-%d %H:%M"),)
        )
    elif is_reminder:
        cursor.execute(
            "SELECT * FROM agendamentos WHERE DATE(data_agendamento) = DATE(?)",
            (reminder_date.strftime("%Y-%m-%d %H:%M"),)
        )
    else:
        cursor.execute("SELECT * FROM agendamentos")
    rows = cursor.fetchall()
    close_connection(connection=conn)
    if rows:
        print(f"Lista de agendamentos: {rows}")
        for row in rows:
            appointment = Appointment(id=row[0], client=get_user(user_id=row[1]), date=row[2])
            appointments.append(appointment)
    else:
        if in_past:
            date = current_date.strftime("%Y-%m-%d")
            NoAppointmentsForSpecifiedPeriod(f"No past appointments when comparing to date: {date}")
        elif in_future:
            date = current_date.strftime("%Y-%m-%d")
            raise NoAppointmentsForSpecifiedPeriod(f"No future appointments when comparing to date: {date}")
        elif is_reminder:
            date=reminder_date.strftime("%Y-%m-%d")
            raise NoAppointmentsForSpecifiedPeriod(f"No appointments reminder for date: {date}")
        else:
            raise NoAppointmentsForSpecifiedPeriod()
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
    try:
        appointment = get_date_appointment(date=datetime.strptime(appointment_date, "%Y-%m-%d %H:%M"))
        print(f"Erro: conflito de horário ao adicionar agendamento. \n{appointment_date} já está agendado para o cliente {appointment.get_client().get_user_name()}.")
    except AppointmentNotFoundException as e:
        cursor.execute(
            "INSERT INTO agendamentos (cliente_id, data_agendamento, data_atualizacao) VALUES (?, ?, ?)", 
            (str(client_id), appointment_date, update_date)
        )
        conn.commit()
        print("Agendamento efetuado com sucesso")
    close_connection(connection=conn)


def delete_appointment(client_name: str, client_email: str, appointment_date: str) -> None:
    """Function to delete User client

    Args:
        name (str): Client name
        email (str): Client email
    """
    conn = start_connection()
    cursor = get_cursor(connection=conn)
    try:
        user = get_user(user_name=client_name, user_email=client_email)
        try:
            appointment = get_user_appointment(user=user, date=appointment_date)
            cursor.execute(
                "DELETE FROM agendamentos WHERE agendamento_id = ?",
                (str(appointment.get_appointment_id()))
            )
            conn.commit()
            print(f"Agendamento de {appointment_date} do usuário {client_name} de e-mail {client_email} deletado com sucesso do banco de dados.")
        except AppointmentNotFoundException as e:
            print(f"Erro ao deletar agendamento:\n{e}")
    except UserNotFoundException as e:
        print(f"Erro ao deletar agendamento:\n{e}")
    finally:
        close_connection(connection=conn)


def update_user_appointment(client_name: str, client_email: str, current_date: str, new_date: str) -> None:
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
        user = get_user(user_name=client_name, user_email=client_email)
        try:
            appointment = get_user_appointment(user=user, date=current_date)
            cursor.execute(
                "UPDATE agendamentos SET data_agendamento = ? WHERE agendamento_id = ?",
                (new_date, str(appointment.get_appointment_id()))
            )
            conn.commit()
            print(f"Agendamento de {current_date} do usuário {client_name} de e-mail {client_email} atualizado com sucesso para {new_date}.")
        except AppointmentNotFoundException as e:
            print(f"Erro ao atualizar agendamento:\n{e}")
    except UserNotFoundException as e:
        print(f"Erro ao atualizar agendamento:\n{e}")
    finally:
        close_connection(connection=conn)

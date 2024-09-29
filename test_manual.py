"""Test manual functions to test the database and the application"""

import time

from dao.agendamento import (
    add_appointment,
    create_table_appointment,
    delete_appointment,
    get_user_appointment,
    list_appointments,
)
from dao.user import (
    create_table_clientes,
    create_user,
    delete_user,
    get_user,
)

from dao.users import (
    create_table_users,
    create_user as create_users,
    delete_user as delete_users,
)
from entities.users import Users
from utils.exceptions import NoAppointmentsForSpecifiedPeriod
from utils.reminders import send_reminder
from utils.util import read_json_asset_file, hash_password


def get_clients_information() -> tuple[str, str]:
    """Function to get client information from a json file

    Returns:
        tuple[str, str]: Tuple with client name and client email
    """
    data = read_json_asset_file(file_name="client_data")
    name = data.get("client_name")
    email = data.get("client_email")
    return name, email


def create_new_user(client_name: str, client_email: str) -> None:
    """Function to create a new user in the database

    Args:
        client_name (_type_): Client name
        client_email (_type_): Client email
    """
    print("Criando tabela de clientes...")
    create_table_clientes()
    print("Deletando cliente se já existir")
    delete_user(client_name, client_email)
    print("Adicionando usuário ao banco de dados...")
    create_user(name=client_name, email=client_email)
    print("Usuário adicionado com sucesso!")
    time.sleep(10)


def get_any_user(client_name: str, client_email: str) -> None:
    """Function to get any user from the database

    Args:
        client_name (str): Client name
        client_email (str): Client email
    """
    print("Requisitando usuário do banco de dados...")
    user = get_user(user_name=client_name, user_email=client_email)
    print("Dados do cliente no banco de dados:")
    print(f"Nome: {user.get_user_name()}")
    print(f"ID: {user.get_user_id()}")
    print(f"E-mail: {user.get_user_email()}")
    time.sleep(10)


def create_new_appointment(client_name: str, client_email: str, date: str) -> None:
    """Function to create a new appointment for a client

    Args:
        client_name (str): Client name
        client_email (str): Client email
        date (str): Appointment date
    """
    print("Criando tabela de agendamento...")
    create_table_appointment()
    print(f"Adicionando novo agendamento para o cliente {client_name}...")
    # Get client
    user = get_user(user_name=client_name, user_email=client_email)
    # Add appointment
    add_appointment(appointment_date=date, user=user)
    time.sleep(10)


def get_next_appointment(client_name: str, client_email: str) -> None:
    """Function to get the next appointment for a client

    Args:
        client_name (str): Client name
        client_email (str): Client email
    """
    print(f"Requisitando o próximo agendamento do cliente {client_name}")
    client = get_user(user_name=client_name, user_email=client_email)
    agendamento = get_user_appointment(user=client)
    print(
        f"Próximo agendamento do cliente {client.get_user_name()} é em {agendamento.get_appointment_date()}"
    )
    time.sleep(10)


def get_appointment(client_name: str, client_email: str, data_agendamento: str) -> None:
    """Function to get the appointment for a client after a specified date

    Args:
        client_name (str): Client name
        client_email (str): Client email
        data_agendamento (str): Date to get the appointment
    """
    print(f"Requisitando o agendamento do cliente {client_name} em {data_agendamento}")
    client = get_user(user_name=client_name, user_email=client_email)
    agendamento = get_user_appointment(user=client, date=data_agendamento)
    print(
        f"Primeiro agendamento do cliente {client.get_user_name()} após {data_agendamento} é em {agendamento.get_appointment_date()}"
    )
    time.sleep(10)


def get_list_all_appointments() -> None:
    """Function to get all appointments from the database"""
    try:
        print("A lista de todos os agendamentos já realizados é: ")
        list_appointments(in_past=True)
        time.sleep(5)
    except NoAppointmentsForSpecifiedPeriod as e:
        print(e)
    try:
        print("A lista de todos os agendamentos futuros é:")
        list_appointments(in_future=True)
        time.sleep(5)
    except NoAppointmentsForSpecifiedPeriod as e:
        print(e)
    try:
        print("A lista de todos os agendamentos de lembretes é: ")
        list_appointments(is_reminder=True)
        time.sleep(5)
    except NoAppointmentsForSpecifiedPeriod as e:
        print(e)
    try:
        print("A lista de todos os agendamento é: ")
        list_appointments()
        time.sleep(5)
    except NoAppointmentsForSpecifiedPeriod as e:
        print(e)


def send_reminder_email() -> None:
    """Function to send a reminder to the next user appointment"""
    # Send reminder to session
    print("Enviando lembretes das sessões de amanhã.")
    send_reminder()
    time.sleep(30)


def delete_user_appointment(
    client_name: str, client_email: str, data_agendamento: str
) -> None:
    """Function to delete a user appointment

    Args:
        client_name (str): Client name
        client_email (str): Client email
        data_agendamento (str): Appointment date
    """
    # Delete user appointment
    print(f"Deletando o agendamento de {data_agendamento} do cliente {client_name}...")
    delete_appointment(
        client_name=client_name,
        client_email=client_email,
        appointment_date=data_agendamento,
    )
    time.sleep(10)


def delete_user_from_database(client_name: str, client_email: str) -> None:
    """Function to delete a user from the database

    Args:
        client_name (str): Client name
        client_email (str): Client email
    """
    print(f"Deletando o usuário {client_name}...")
    delete_user(client_name, client_email)
    time.sleep(10)


def handle_users_table() -> None:
    """Function to handle users table"""
    data = read_json_asset_file(file_name="users_data")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    password = hash_password(data.get("password"))
    birth_date = data.get("birth_date")
    create_table_users()
    time.sleep(10)
    create_users(first_name, last_name, email, password, birth_date)
    time.sleep(10)


if __name__ == "__main__":
    # Create users table
    handle_users_table()
    # delete_users(1)

    # GET CLIENTS INFORMATION
    # client_name, client_email = get_clients_information()
    # Add a new client - SUCCESSFULLY TESTED
    # create_new_user(client_name, client_email)

    # Delete a client - SUCCESSFULLY TESTED
    # delete_user_from_database(client_name, client_email)

    # Get a client information - SUCCESSFULLY TESTED
    # get_any_user(client_name, client_email)

    # Create a new appointment - SUCCESSFULLY TESTED
    # create_new_appointment(client_name, client_email, "2024-09-20 15:00")

    # Get client next appointment - SUCCESSFULLY TESTED
    # get_next_appointment(client_name, client_email)

    # Get client appointment - SUCCESSFULLY TESTED
    # get_appointment(client_name, client_email, "2024-09-26 16:00")

    # List all appointments - SUCCESSFULLY TESTED
    # get_list_all_appointments()

    # Delete appointment - SUCCESSFULLY TESTED
    # delete_user_appointment(client_name, client_email, "2024-09-26 16:00")

    # Send a reminder for next user appointment - SUCCESSFULLY TESTED
    # send_reminder_email()

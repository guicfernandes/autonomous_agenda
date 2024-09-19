from dao.agendamento import get_user_appointment, list_appointments, add_appointment, create_table_appointment, delete_appointment
from dao.user import get_user, create_user, create_table_user, delete_user
from utils.exceptions import NoAppointmentsForSpecifiedPeriod
from utils.reminders import send_reminder
from utils.util import read_json_asset_file
import time


def get_clients_information():
    data = read_json_asset_file(file_name='client_data')
    client_name = data['client_name']
    client_email = data['client_email']
    return client_name, client_email


def create_new_user(client_name, client_email):
    print('Criando tabela de clientes...')
    create_table_user()
    print('Deletando cliente se já existir')
    delete_user(client_name, client_email)
    print('Adicionando usuário ao banco de dados...')
    create_user(name=client_name, email=client_email)
    print("Usuário adicionado com sucesso!")
    time.sleep(10)


def get_any_user(client_name, client_email):
    print('Requisitando usuário do banco de dados...')
    user = get_user(user_name=client_name, user_email=client_email)
    print(f"Dados do cliente no banco de dados:")
    print(f"Nome: {user.get_user_name()}")
    print(f"ID: {user.get_user_id()}")
    print(f"E-mail: {user.get_user_email()}")
    time.sleep(10)


def create_new_appointment(client_name, client_email, date):
    print('Criando tabela de agendamento...')
    create_table_appointment()
    print(f'Adicionando novo agendamento para o cliente {client_name}...')
    # Get client
    user = get_user(user_name=client_name, user_email=client_email)
    # Add appointment
    add_appointment(appointment_date=date, user=user)
    time.sleep(10)


def get_next_appointment(client_name, client_email):
    print(f'Requisitando o próximo agendamento do cliente {client_name}')
    client = get_user(user_name=client_name, user_email=client_email)
    agendamento = get_user_appointment(user=client)
    print(f"Próximo agendamento do cliente {client.get_user_name()} é em {agendamento.get_appointment_date()}")
    time.sleep(10)


def get_appointment(client_name, client_email, data_agendamento):
    print(f'Requisitando o agendamento do cliente {client_name} em {data_agendamento}')
    client = get_user(user_name=client_name, user_email=client_email)
    agendamento = get_user_appointment(user=client, date=data_agendamento)
    print(f"Primeiro agendamento do cliente {client.get_user_name()} após {data_agendamento} é em {agendamento.get_appointment_date()}")
    time.sleep(10)


def get_list_all_appointments():
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


def send_reminder_email():
    # Send reminder to session
    print("Enviando lembretes das sessões de amanhã.")
    send_reminder()
    time.sleep(30)


def delete_user_appointment(client_name, client_email, data_agendamento):
    # Delete user appointment
    print(f'Deletando o agendamento de {data_agendamento} do cliente {client_name}...')
    delete_appointment(client_name=client_name, client_email=client_email, appointment_date=data_agendamento)
    time.sleep(10)


def delete_user_from_database(client_name, client_email):
    print(f'Deletando o usuário {client_name}...')
    delete_user(client_name, client_email)
    time.sleep(10)


if "__main___":
    client_name, client_email = get_clients_information()
    # Add a new user - SUCCESSFULLY TESTED
    # create_new_user(client_name, client_email)

    # Delete a user - SUCCESSFULLY TESTED
    # delete_user_from_database(client_name, client_email)

    # Get a user information - SUCCESSFULLY TESTED
    # get_any_user(client_name, client_email)
    
    # Create a new appointment - SUCCESSFULLY TESTED
    # create_new_appointment(client_name, client_email, "2024-09-20 15:00")
    
    # Get user next appointment - SUCCESSFULLY TESTED
    # get_next_appointment(client_name, client_email)

    # Get user appointment - SUCCESSFULLY TESTED
    # get_appointment(client_name, client_email, "2024-09-26 16:00")
    
    # List all appointments - SUCCESSFULLY TESTED
    get_list_all_appointments()

    # Delete appointment - SUCCESSFULLY TESTED
    # delete_user_appointment(client_name, client_email, "2024-09-26 16:00")

    # Send a reminder for next user appointment - SUCCESSFULLY TESTED
    # send_reminder_email()
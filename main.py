from dao.agendamento import get_user_next_appointment, list_appointments, add_appointment
from dao.user import get_user, add_user
from utils.reminders import send_reminder
import time

# CHANGE HERE
client_name = "CHANGE ME"
# CHANGE HERE
client_email = "CHANGE ME"
def create_new_user():
    add_user(name=client_name, email=client_email)
    print("Usuário adicionado com sucesso")


def get_any_user():
    user = get_user(user_name=client_name, user_email=client_email)
    print(f"Dados do cliente no banco de dados:")
    print(f"Nome: {user.get_user_name()}")
    print(f"ID: {user.get_user_id()}")
    print(f"E-mail: {user.get_user_email()}")


def create_new_appointment():
    # Get client
    user = get_user(user_name=client_name, user_email=client_email)
    # Add appointment
    add_appointment(appointment_date="2024-09-18 16:00", user=user)
    print("Agendamento efetuado com sucesso")


def get_next_appointment():
    client = get_user(user_name=client_name, user_email=client_email)
    agendamento = get_user_next_appointment(user=client)
    print(f"Próximo agendamento do cliente client {client.get_user_name()} é em {agendamento.get_appointment_date()}")


def get_list_all_appointments():
    print("A lista de todos os agendamentos já realizados é: ")
    list_appointments(in_past=True)
    print("A lista de todos os agendamentos futuros é:")
    list_appointments(in_future=True)
    print("A lista de todos os agendamento é: ")
    list_appointments()


def send_reminder_email():
    # Send reminder to session
    print("Enviando lembretes das sessões de amanhã.")
    send_reminder()


if "__main___":
    # Add a new user
    create_new_user()
    # Get a user information
    time.sleep(10)
    get_any_user()
    time.sleep(10)
    # Create a new appointment
    create_new_appointment()
    time.sleep(10)
    # Get user next appointment
    get_next_appointment()
    time.sleep(30)
    # List all appointments
    get_list_all_appointments()
    time.sleep(60)
    # Send a reminder for next user appointment
    send_reminder_email()
    time.sleep(30)
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dao.agendamento import list_appointments
from utils.contants import BUSINESS_NAME, BUSINESS_OBJECT, BUSINESS_OWNER
from utils.exceptions import NoAppointmentsForSpecifiedPeriod
from utils.util import get_sender_information, get_smtp_data


def send_email(receiver: str, subject: str, body: str) -> None:
    """Function to send an email

    Args:
        receiver (str): Receiver e-mail address
        subject (str): E-mail subject
        body (str): E-mail Body
    """
    sender_email, sender_pass = get_sender_information()
    smtp_server, smtp_port = get_smtp_data()
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        # Conectar ao servidor SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Iniciar TLS
        server.login(sender_email, sender_pass)  # Login
        text = msg.as_string()
        server.sendmail(sender_email, receiver, text)
        server.quit()
        print(f"E-mail enviado para {receiver} com sucesso!")
    except Exception as e:
        print(f"Falha ao enviar e-mail: {e}")

def send_reminder() -> bool:
    """Function to send reminder session to a client
    """
    # Select tomorrow's all appointments
    try:
        appointments = list_appointments(is_reminder=True)
        for appointment in appointments:
            client_name = appointment.get_client().get_user_name()
            client_email = appointment.get_client().get_user_email()
            data_agendamento = appointment.get_appointment_date()
                
            subject = f"Lembrete: {BUSINESS_OBJECT} Amanhã com {BUSINESS_OWNER}"
            body = f"Olá {client_name},\n\nEste é um lembrete da sua {BUSINESS_OBJECT} agendada para {data_agendamento} com {BUSINESS_OWNER}.\n\nAtenciosamente,\n{BUSINESS_NAME}"
                
            send_email(receiver=client_email, subject=subject, body=body)  
            return True  
    except NoAppointmentsForSpecifiedPeriod as e:
        print(f"Não há lembretes a serem enviados para amanhã. {e}")
        return False

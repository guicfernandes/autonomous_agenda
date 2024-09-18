import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from utils.connection import start_connection, close_connection, get_cursor
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

def send_reminder() -> None:
    """Function to send reminder session to a client
    """
    # Definir a hora atual e a hora de um dia antes
    current_date = datetime.now()
    reminder_date = current_date + timedelta(days=1)
    conn = start_connection()
    cursor = get_cursor(connection=conn)

    cursor.execute("SELECT * FROM agendamentos WHERE data_agendamento BETWEEN ? AND ?", 
              (current_date.strftime("%Y-%m-%d %H:%M"), reminder_date.strftime("%Y-%m-%d %H:%M")))
    appointments = cursor.fetchall()
    
    for appointment in appointments:
        client_id = appointment[1]
        data_agendamento = appointment[2]
        client = cursor.execute("SELECT * FROM clientes WHERE cliente_id = ?", client_id)
        client_name = client[1]
        client_email = client[2]
        
        subject = "Lembrete: Consulta de Psicologia Amanhã"
        body = f"Olá {client_name},\n\nEste é um lembrete da sua consulta de psicologia agendada para {data_agendamento}.\nDetalhes: {detalhes}\n\nAtenciosamente,\nSua Clínica"
        
        send_email(client_email, subject, body)
    close_connection(connection=conn)

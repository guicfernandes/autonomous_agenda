from flask import Flask, render_template, redirect, url_for
from dao.agendamento import list_appointments
from utils.reminders import send_reminder

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'  # Needed for flash messages
    # TODO: how to set the secret key in flask?

    from .users.routes import users_bp
    from .appointments.routes import appointments_bp
    from .agenda.routes import agenda_bp

    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(appointments_bp, url_prefix='/appointments')
    app.register_blueprint(agenda_bp, url_prefix='/agenda')

    @app.route('/')
    def home():
        today_appointments = list_appointments(is_today=True)
        return render_template('index.html', today_appointments=today_appointments)

    @app.route('/send_reminders')
    def send_reminders():
        if send_reminder():
            # return redirect(url_for('home', reminder_sent='true'))
            reminder_sent = 'true'
        else:
            # return redirect(url_for('home', reminder_error='true'))
            reminder_sent = 'false'
        return redirect(url_for('home', reminder_sent=reminder_sent))

    return app
"""
    @app.route('/users')
    def users():
        # users = list_users()
        # return render_template('user/index.html', users=users)
        # return render_template('users/index.html')
        return redirect(url_for('users.users_home', added='true'))

    @app.route('/appointments')
    def appointments():
        # Implement the logic to fetch and display appointments
        return render_template('appointments/index.html')

    @app.route('/agenda')
    def agenda():
        # Implement the logic to fetch and display agenda
        return render_template('agenda/index.html')
    
    return app
"""

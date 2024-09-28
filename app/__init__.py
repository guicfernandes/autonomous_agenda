"""Module to create the Flask app and define the routes"""

from flask import Flask, render_template, redirect, request, url_for, flash
from dao.agendamento import list_appointments
from utils.reminders import send_reminder
from .forms import LoginForm, RegisterForm
from .users.routes import users_bp
from .appointments.routes import appointments_bp
from .agenda.routes import agenda_bp
from utils.exceptions import NoAppointmentsForSpecifiedPeriod


def create_app() -> Flask:
    """Function to create the Flask app

    Returns:
        Flask: Flask application
    """
    app = Flask(__name__)
    app.secret_key = "your_secret_key"  # Needed for flash messages
    # TODO: how to set the secret key in flask?

    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(appointments_bp, url_prefix="/appointments")
    app.register_blueprint(agenda_bp, url_prefix="/agenda")

    # TODO: move routes to separate route.py module
    @app.route("/")
    @app.route("/index")
    ## TODO: needs to change to home and create a index page
    def index():
        return render_template("index.html", logged=False)

    @app.route("/home")
    def home():
        try:
            today_appointments = list_appointments(is_today=True)
            return render_template("home.html", today_appointments=today_appointments)
        except NoAppointmentsForSpecifiedPeriod as e:
            print(f"No appointments found: {e.message}")
            return render_template("home.html", no_appointments="true")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            # TODO: implement login logic to check if it was successful
            if request.form.get("email") == "aaa@email.com":
                flash("You are successfully logged in", category="success")
                return redirect(url_for("home"))
            flash(
                "Login Unsuccessful. Please check email and password",
                category="danger",
            )
        return render_template("login.html", form=form, logged="false")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        form = RegisterForm()
        # TODO: implement register logic
        return render_template("register.html", form=form, logged=False)

    @app.route("/send_reminders")
    def send_reminders():
        if send_reminder():
            reminder_sent = "true"
        else:
            reminder_sent = "false"
        return redirect(url_for("home", reminder_sent=reminder_sent))

    return app

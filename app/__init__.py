"""Module to create the Flask app and define the routes"""

from flask import Flask, flash, redirect, render_template, url_for
from flask_wtf.csrf import CSRFProtect
from wtforms.validators import ValidationError
from flask_talisman import Talisman

from dao.agendamento import list_appointments
from utils.exceptions import NoAppointmentsForSpecifiedPeriod
from utils.reminders import send_reminder

from .agenda.routes import agenda_bp
from .appointments.routes import appointments_bp
from .forms import LoginForm, RegisterForm
from .users.routes import users_bp


def create_app() -> Flask:
    """Function to create the Flask app

    Returns:
        Flask: Flask application
    """
    app = Flask(__name__)
    app.secret_key = "your_secret_key"  # Needed for flash messages
    # TODO: how to set the secret key in flask?

    # Enable CSRF protection
    csrf = CSRFProtect(app)

    # Add security headers
    # Talisman(app)

    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(appointments_bp, url_prefix="/appointments")
    app.register_blueprint(agenda_bp, url_prefix="/agenda")

    # TODO: move routes to separate route.py module
    @app.route("/")
    @app.route("/index")
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
            try:
                if form.validate_user(
                    email=form.email.data, password=form.password.data
                ):
                    flash("You are successfully logged in", category="success")
                    return redirect(url_for("home"))
            except ValidationError as e:
                flash(e, category="danger")
        return render_template("login.html", form=form, logged=False)

    @app.route("/register", methods=["GET", "POST"])
    def register():
        form = RegisterForm()
        if form.validate_on_submit():
            try:
                if form.validate_registration():
                    flash("Registration successful", category="success")
                    return redirect(url_for("login"))
            except ValidationError as e:
                flash(e, category="danger")
        return render_template("register.html", form=form, logged=False)

    @app.route("/send_reminders")
    def send_reminders():
        if send_reminder():
            reminder_sent = "true"
        else:
            reminder_sent = "false"
        return redirect(url_for("home", reminder_sent=reminder_sent))

    return app

from flask import Blueprint, render_template, request, redirect, url_for
from dao.agendamento import list_appointments

appointments_bp = Blueprint('appointments', __name__, template_folder='templates')

@appointments_bp.route('/')
def appointments_home():
    appointments = list_appointments(is_today=True)
    return render_template('appointments/index.html', appointments=appointments)
from flask import Blueprint, render_template, request, redirect, url_for
from dao.agendamento import list_appointments

agenda_bp = Blueprint('agenda', __name__, template_folder='templates')

@agenda_bp.route('/')
def agenda_home():
    agenda = list_appointments()
    return render_template('agenda/index.html', agenda=agenda)
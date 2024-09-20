from flask import Blueprint, render_template, request, redirect, url_for
from dao.user import list_users, create_user, delete_user, update_user, get_user

users_bp = Blueprint('users', __name__, template_folder='templates')

@users_bp.route('/')
def users_home():
    users = list_users()
    return render_template('users/index.html', users=users)

@users_bp.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        client_name = request.form['client_name']
        client_email = request.form['client_email']
        create_user(name=client_name, email=client_email)
        return redirect(url_for('users.users_home', added='true'))
    return render_template('users/add.html')

@users_bp.route('/update/<client_id>', methods=['GET', 'POST'])
def update_user_route(client_id):
    if request.method == 'POST':
        new_email = request.form['client_email']
        update_user(id=client_id, new_email=new_email)
        return redirect(url_for('users.users_home', updated='true'))
    user = get_user(user_id=client_id)
    return render_template('users/update.html', user=user)

@users_bp.route('/delete/<client_id>')
def delete_user_route(client_id: str):
    delete_user(id=client_id)
    return redirect(url_for('users.users_home', deleted='true'))

@users_bp.route('/details/<client_id>')
def details_user_route(client_id: str):
    user = get_user(user_id=client_id)
    return render_template('users/details.html', user=user)

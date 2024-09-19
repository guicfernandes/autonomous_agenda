from flask import Flask, render_template, request, redirect, url_for
from dao.user import list_users, create_user, delete_user, update_user, get_user

app = Flask(__name__)

@app.route('/')
def index():
    users = list_users()
    return render_template('user/index.html', users=users)

@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        client_name = request.form['client_name']
        client_email = request.form['client_email']
        create_user(name=client_name, email=client_email)
        return redirect(url_for('index', added='true'))
    return render_template('user/add_user.html')

@app.route('/update/<client_id>', methods=['GET', 'POST'])
def update_user_route(client_id):
    if request.method == 'POST':
        new_email = request.form['client_email']
        update_user(id=client_id, new_email=new_email)
        return redirect(url_for('index', updated='true'))
    user = get_user(user_id=client_id)
    return render_template('user/update_user.html', user=user)

@app.route('/delete/<client_id>')
def delete_user_route(client_id: str):
    delete_user(id=client_id)
    return redirect(url_for('index', deleted='true'))

@app.route('/details/<client_id>')
def details_user_route(client_id: str):
    user = get_user(user_id=client_id)
    return render_template('user/details.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)
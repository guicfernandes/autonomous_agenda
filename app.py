from flask import Flask, render_template, request, redirect, url_for
from dao.user import list_users, create_user, delete_user, update_user

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
        return redirect(url_for('index'))
    return render_template('user/add_user.html')

@app.route('/update/<client_name>/<client_email>', methods=['GET', 'POST'])
def update_user_route(client_name, client_email):
    if request.method == 'POST':
        new_email = request.form['client_email']
        update_user(name=client_name, current_email=client_email, new_email=new_email)
        return redirect(url_for('index'))
    return render_template('user/update_user.html', client_name=client_name, client_email=client_email)

@app.route('/delete/<client_name>/<client_email>')
def delete_user_route(client_name, client_email):
    delete_user(client_name, client_email)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
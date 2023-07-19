from flask import Flask, render_template, request, redirect,Blueprint

login = Blueprint('login', __name__)

@login.route('/login', methods=['GET', 'POST'])
def login_adm():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Aqui você pode verificar as credenciais do usuário

        # Exemplo de verificação simples de usuário e senha
        if username == 'admin' and password == 'admin':
            return redirect('/admin')
        else:
            return render_template('login.html', error='Credenciais inválidas')

    return render_template('login.html', error=None)




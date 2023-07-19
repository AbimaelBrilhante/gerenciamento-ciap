from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = 'ciap-3c'

@app.route('/')
def index():
    return render_template('index.html')

from ciap.routes import ciap
from sped.routes import sped
from login.routes import login
from admin.routes import admin

app.register_blueprint(ciap)
app.register_blueprint(sped)
app.register_blueprint(login)
app.register_blueprint(admin)


if __name__ == '__main__':
    app.secret_key = 'ciap-3c'
    app.run(debug=True)




from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, template_folder=
            'C:/Users/Administrator/Desktop/coisas/flask_project/templates',
            static_folder='C:/Users/Administrator/Desktop/coisas/flask_project/static'
            )

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class users(db.Model):
    id = db.Column("id", db.Integer, primary_key = True)
    email = db.Column(db.String(100))
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    message = db.Column(db.String(100))


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/cadastro",  methods=['GET', 'POST'])
def cadastro():
    try:
        if request.method == 'POST':
            email = request.form['email']
            name = request.form['name']
            password = request.form['password']
            message = request.form['message']
            usuarios =  users(email = email, name = name, password = password, message = message)
            db.session.add(usuarios)
            db.session.commit()
            return redirect('/')  
    except Exception as e:
        print('Erro', e)


@app.route("/<int:id>/edit", methods=['GET', 'POST'])
def editar(id):
    try:
        usuario = users.query.filter_by(id=id).first()
        if request.method == 'POST':
            if usuario:
                # Delete the old user
                db.session.delete(usuario)
                db.session.commit()

                # Create a new user with the updated data
                email = request.form['email']
                name = request.form['name']
                password = request.form['password']
                message = request.form['message']
                usuario = users(
                    email=email,
                    name=name,
                    password=password,
                    message=message
                )
                db.session.add(usuario)
                db.session.commit()
                return redirect('/')
        return render_template('edit.html', usuario=usuario)
    except Exception as e:
        print('Erro', e)
        return None
    

@app.route('/<int:id>/delete')
def delete(id):
    usuario = users.query.filter_by(id=id).first()
    db.session.delete(usuario)
    db.session.commit()
    return redirect('/')

@app.route("/show", methods = ["GET"])
def show():
    usuarios = users.query.all()
    return render_template('show.html', usuarios = usuarios)

if __name__ == '__main__':
    app.run(debug=True)
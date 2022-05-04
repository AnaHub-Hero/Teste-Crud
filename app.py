from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///problemas.sqlite3'
db = SQLAlchemy(app)


class Problema(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    codigo = db.Column(db.String(10), nullable=False)
    rua = db.Column(db.String(50), nullable=False)
    bairro = db.Column(db.String(50), nullable=False)
    cidade = db.Column(db.String(50), nullable=False)
    problema = db.Column(db.String(300), nullable=False)

    def __init__(self, nome, email, codigo, rua, bairro, cidade, problema):
        self.nome = nome
        self.email = email
        self.codigo = codigo
        self.rua = rua
        self.bairro = bairro
        self.cidade = cidade
        self.problema = problema


@app.route('/')
def index():
    problemas = Problema.query.all()
    return render_template('index.html', problemas=problemas)


@app.route('/<id>')
def informa_pelo_id(id):
   informa = Problema.query.get(id)
   return render_template('index.html', informa=informa)


@app.route('/novo', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        informa = Problema(request.form['nome'], request.form['email'], request.form['codigo'], request.form['rua'], request.form['bairro'], request.form['cidade'], request.form['problema'])
        db.session.add(informa)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('novo.html')


@app.route('/edita/<int:id>', methods=['GET', 'POST'])
def edit(id):
    informa = Problema.query.get(id)
    if request.method == 'POST':
        informa.nome = request.form['nome']
        informa.email = request.form['email']
        informa.codigo = request.form['codigo']
        informa.rua = request.form['rua']
        informa.bairro = request.form['bairro']
        informa.cidade = request.form['cidade']
        informa.problema = request.form['problema']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edita.html', informa=informa)


@app.route('/delete/<int:id>')
def delete(id):
    informa = Problema.query.get(id)
    db.session.delete(informa)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

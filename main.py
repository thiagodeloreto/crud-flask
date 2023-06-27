from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
db = SQLAlchemy(app)

class Estudante(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  nome = db.Column(db.String(150))
  idade = db.Column(db.Integer)

  def __init__(self,nome, idade):
    self.nome = nome
    self.idade = idade

@app.route('/')
def index():
  estudantes = Estudante.query.all()
  return render_template('index.html', estudantes=estudantes)

@app.route("/add", methods=['GET', 'POST'])
def add():
  if request.method == 'POST':
    estudante = Estudante(request.form['nome'], request.form['idade'])
    db.session.add(estudante)
    db.session.commit()
    return redirect(url_for('index'))
  if request.method == 'GET':
    return render_template('add.html')

@app.route("/delete/<int:id>", methods=['GET', 'POST'])
def delete(id):
  estudante = Estudante.query.get(id)
  db.session.delete(estudante)
  db.session.commit()
  return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
      estudante = Estudante.query.get(id)
      if request.method == 'POST':
        estudante.nome = request.form['nome']
        estudante.idade = request.form['idade']
        db.session.commit()
        return redirect(url_for('index'))
      return render_template('edit.html', estudante=estudante)


if __name__ == '__main__':
  with app.app_context():
    db.create_all()
  app.run(host='0.0.0.0', port=8000, debug=True)

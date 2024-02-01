from flask import *
from flask_sqlalchemy import SQLAlchemy as _BaseSQLAlchemy
from sqlalchemy import desc, asc, func
from sqlalchemy.orm import joinedload
from tables import *
from datetime import datetime, date, timedelta

class SQLAlchemy(_BaseSQLAlchemy):
    def apply_pool_defaults(self, app, options):
        super(SQLAlchemy, self).apply_pool_defaults(self, app, options)
        options["pool_pre_ping"] = True

db = SQLAlchemy()
app = Flask(__name__, template_folder='./templates')

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True}  

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:ROOT@localhost/crud_basico"

app.config["SECRET_KEY"] = 'secret'
db.init_app(app)

#HOME
@app.route('/home', methods=['GET', 'POST'])
def home():
    alunos = db.session.query(Alunos).all()
    
    return render_template('home.html', alunos=alunos)

#INSERT
@app.route('/cadastrar_novo_aluno', methods=['GET', 'POST'])
def cadastrar_novo_aluno():
    dados_dict = request.get_json()

    if request.method == 'POST':
        novo_aluno = Alunos(nome = dados_dict[0]['nome'], email =dados_dict[0]['email'], telefone=dados_dict[0]['telefone'],
                            idade = dados_dict[0]['idade'], data_nascimento = dados_dict[0]['data_nascimento'])
        db.session.add(novo_aluno)
        db.session.commit()

        flash('Novo cadastro realizado com sucesso')

        return redirect(url_for('home'))


#EDITAR
@app.route('/editar_registro/<int:aluno_id>', methods =['GET', 'POST'])
def editar_registro(aluno_id):
    aluno = db.session.query(Alunos).filter(Alunos.id==aluno_id).first()
    dados_aluno = request.get_json()

    if request.method == 'POST':
        aluno.nome = dados_aluno[0]['nome']
        aluno.email = dados_aluno[0]['email']
        aluno.telefone = dados_aluno[0]['telefone']
        aluno.idade = dados_aluno[0]['idade']
        aluno.data_nascimento = dados_aluno[0]['data_nascimento']

        db.session.commit()

        flash(f'Registro referente ao aluno {aluno.nome} atualizado com sucesso!')

        return redirect(url_for('home'))
    

#DELETAR
@app.route('/deletar_registro/<int:aluno_id>', methods = ['GET', 'POST'])
def deletar_registro(aluno_id):
    aluno = db.session.query(Alunos).filter(Alunos.id==aluno_id).first()
    db.session.delete(aluno)
    db.session.commit()

    flash('Registro excluído com sucesso')

    return redirect(url_for('home'))


if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0')
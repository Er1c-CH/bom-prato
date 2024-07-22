from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class CartaoDependencia(db.Model):
    __tablename__ = 'cartao_dependencia'
    id_cartao = db.Column(db.Integer, primary_key=True)
    validade = db.Column(db.Date, nullable=False)
    pontos = db.Column(db.Integer, default=0)
    data_emissao = db.Column(db.Date, nullable=False)

class Cliente(db.Model):
    __tablename__ = 'cliente'
    id_cliente = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    id_cartao = db.Column(db.Integer, db.ForeignKey('cartao_dependencia.id_cartao', ondelete='SET NULL', onupdate='CASCADE'))

class Pedido(db.Model):
    __tablename__ = 'pedido'
    id_pedido = db.Column(db.Integer, primary_key=True)
    id_prato = db.Column(db.Integer, db.ForeignKey('prato.id_prato', ondelete='CASCADE', onupdate='CASCADE'))
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id_cliente', ondelete='CASCADE', onupdate='CASCADE'))
    horario_pedido = db.Column(db.DateTime, nullable=False)

class Ingrediente(db.Model):
    __tablename__ = 'ingrediente'
    id_ingrediente = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    quantidade = db.Column(db.Integer, default=0)

class Funcionario(db.Model):
    id_funcionario = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    cargo = db.Column(db.String(50), nullable=False)
    turno = db.Column(db.String(20), nullable=False)
    salario = db.Column(db.Numeric(10, 2), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)

class Prato(db.Model):
    __tablename__ = 'prato'
    id_prato = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Numeric(10, 2), nullable=False)

class PratoIngrediente(db.Model):
    __tablename__ = 'prato_ingrediente'
    id_prato = db.Column(db.Integer, db.ForeignKey('prato.id_prato', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    id_ingrediente = db.Column(db.Integer, db.ForeignKey('ingrediente.id_ingrediente', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    quantidade_utilizada = db.Column(db.Integer, nullable=False)

class Telefone(db.Model):
    __tablename__ = 'telefone'
    id_fornecedor = db.Column(db.Integer, db.ForeignKey('fornecedor.id_fornecedor', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    numero = db.Column(db.String(15), primary_key=True)

class Fornecedor(db.Model):
    __tablename__ = 'fornecedor'
    id_fornecedor = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

class FornecedorIngrediente(db.Model):
    __tablename__ = 'fornecedor_ingrediente'
    id_fornecedor = db.Column(db.Integer, db.ForeignKey('fornecedor.id_fornecedor', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    id_ingrediente = db.Column(db.Integer, db.ForeignKey('ingrediente.id_ingrediente', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    preco_fornecido = db.Column(db.Numeric(10, 2), nullable=False)

class HistoricoEntrega(db.Model):
    __tablename__ = 'historico_entrega'
    id_entrega = db.Column(db.Integer, primary_key=True)
    id_fornecedor = db.Column(db.Integer, db.ForeignKey('fornecedor.id_fornecedor', ondelete='CASCADE', onupdate='CASCADE'))
    id_ingrediente = db.Column(db.Integer, db.ForeignKey('ingrediente.id_ingrediente', ondelete='CASCADE', onupdate='CASCADE'))
    data_entrega = db.Column(db.Date, nullable=False)
    quantidade_entregue = db.Column(db.Integer, nullable=False)

class HistoricoPedido(db.Model):
    __tablename__ = 'historico_pedido'
    id_historico = db.Column(db.Integer, primary_key=True)
    id_pedido = db.Column(db.Integer, db.ForeignKey('pedido.id_pedido', ondelete='CASCADE', onupdate='CASCADE'))
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id_cliente', ondelete='CASCADE', onupdate='CASCADE'))
    data_pedido = db.Column(db.DateTime, nullable=False)
    detalhes_pedido = db.Column(db.Text)

class LoginFuncionario(db.Model):
    __tablename__ = 'login_funcionario'
    id_login = db.Column(db.Integer, primary_key=True)
    id_funcionario = db.Column(db.Integer, db.ForeignKey('funcionario.id_funcionario', ondelete='CASCADE', onupdate='CASCADE'))
    username = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    ultimo_login = db.Column(db.DateTime)

    def set_password(self, senha):
        self.senha = generate_password_hash(senha)

    def check_password(self, senha):
        return check_password_hash(self.senha, senha)
    
class HistoricoCriacaoPedido(db.Model):
    __tablename__ = 'historico_criacao_pedido'
    id_historico = db.Column(db.Integer, primary_key=True)
    id_pedido = db.Column(db.Integer, db.ForeignKey('pedido.id_pedido', ondelete='CASCADE', onupdate='CASCADE'))
    id_funcionario = db.Column(db.Integer, db.ForeignKey('funcionario.id_funcionario', ondelete='CASCADE', onupdate='CASCADE'))
    data_criacao = db.Column(db.DateTime, nullable=False)

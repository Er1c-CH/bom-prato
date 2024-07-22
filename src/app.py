from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config
from models import db

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

db.init_app(app)

jwt = JWTManager(app)

# Importar e registrar blueprints
from routes.fornecedor_ingrediente import fornecedor_ingrediente_bp
from routes.prato_ingrediente import prato_ingredientes_bp
from routes.funcionarios import funcionarios_bp
from routes.ingredientes import ingredientes_bp
from routes.fornecedor import fornecedor_bp
from routes.clientes import clientes_bp
from routes.pedidos import pedidos_bp
from routes.pratos import pratos_bp
from routes.auth import auth_bp

app.register_blueprint(fornecedor_ingrediente_bp)
app.register_blueprint(prato_ingredientes_bp)
app.register_blueprint(funcionarios_bp)
app.register_blueprint(ingredientes_bp)
app.register_blueprint(fornecedor_bp)
app.register_blueprint(clientes_bp)
app.register_blueprint(pedidos_bp)
app.register_blueprint(pratos_bp)
app.register_blueprint(auth_bp)

@app.route('/')
def index():
    return "Seja bem-vindo ao Bom Prato!"

if __name__ == '__main__':
    app.run(debug=True)

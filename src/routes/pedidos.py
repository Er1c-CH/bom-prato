from flask import Blueprint, request, jsonify
from sqlalchemy import text
from models import db

pedidos_bp = Blueprint('pedidos', __name__, url_prefix='/pedidos')

@pedidos_bp.route('', methods=['POST'])
def create_pedido():
    data = request.get_json()
    id_prato = data.get('id_prato')
    id_cliente = data.get('id_cliente')
    horario_pedido = data.get('horario_pedido')

    sql_insert_query = text("""
    INSERT INTO pedido (id_prato, id_cliente, horario_pedido)
    VALUES (:id_prato, :id_cliente, :horario_pedido)
    RETURNING id_pedido;
    """)
    result = db.session.execute(sql_insert_query, {'id_prato': id_prato, 'id_cliente': id_cliente, 'horario_pedido': horario_pedido})
    db.session.commit()

    id_pedido = result.fetchone()[0]

    return jsonify({'message': 'Pedido criado com sucesso!', 'id_pedido': id_pedido}), 201

@pedidos_bp.route('/<int:id>', methods=['GET'])
def get_pedido(id):
    sql_query = text("""
    SELECT id_pedido, id_prato, id_cliente, horario_pedido
    FROM pedido
    WHERE id_pedido = :id;
    """)
    result = db.session.execute(sql_query, {'id': id})
    pedido = result.mappings().fetchone()

    if pedido:
        return jsonify({
            'id_pedido': pedido['id_pedido'],
            'id_prato': pedido['id_prato'],
            'id_cliente': pedido['id_cliente'],
            'horario_pedido': pedido['horario_pedido']
        })
    else:
        return jsonify({'message': 'Pedido não encontrado'}), 404

@pedidos_bp.route('', methods=['GET'])
def get_pedidos():
    sql_query = text("""
    SELECT id_pedido, id_prato, id_cliente, horario_pedido
    FROM pedido;
    """)
    result = db.session.execute(sql_query)
    pedidos = result.mappings().fetchall()

    pedidos_list = [{
        'id_pedido': pedido['id_pedido'],
        'id_prato': pedido['id_prato'],
        'id_cliente': pedido['id_cliente'],
        'horario_pedido': pedido['horario_pedido']
    } for pedido in pedidos]

    return jsonify(pedidos_list)

@pedidos_bp.route('/<int:id>', methods=['PUT'])
def update_pedido(id):
    data = request.get_json()
    id_prato = data.get('id_prato')
    id_cliente = data.get('id_cliente')
    horario_pedido = data.get('horario_pedido')

    sql_check_query = text("SELECT COUNT(1) FROM pedido WHERE id_pedido = :id;")
    result = db.session.execute(sql_check_query, {'id': id})
    if result.fetchone()[0] == 0:
        return jsonify({'message': 'Pedido não encontrado'}), 404

    sql_update_query = text("""
    UPDATE pedido
    SET id_prato = COALESCE(:id_prato, id_prato),
        id_cliente = COALESCE(:id_cliente, id_cliente),
        horario_pedido = COALESCE(:horario_pedido, horario_pedido)
    WHERE id_pedido = :id;
    """)
    db.session.execute(sql_update_query, {'id_prato': id_prato, 'id_cliente': id_cliente, 'horario_pedido': horario_pedido, 'id': id})
    db.session.commit()

    return jsonify({'message': 'Pedido atualizado com sucesso!'})

@pedidos_bp.route('/<int:id>', methods=['DELETE'])
def delete_pedido(id):
    sql_check_query = text("SELECT COUNT(1) FROM pedido WHERE id_pedido = :id;")
    result = db.session.execute(sql_check_query, {'id': id})
    if result.fetchone()[0] == 0:
        return jsonify({'message': 'Pedido não encontrado'}), 404

    sql_delete_query = text("DELETE FROM pedido WHERE id_pedido = :id;")
    db.session.execute(sql_delete_query, {'id': id})
    db.session.commit()

    return jsonify({'message': 'Pedido deletado com sucesso!'})

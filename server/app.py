#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    all_bakeries = Bakery.query.all()
    bakery_list = []
    for bakery in all_bakeries:
        bakery_data = bakery.to_dict(rules=('-baked_goods.bakery',))
        bakery_data['baked_goods'] = [baked_good.to_dict() for baked_good in bakery.baked_goods]
        bakery_list.append(bakery_data)

    response = make_response(jsonify(bakery_list))
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get(id)
    if bakery:
        bakery_data = bakery.to_dict()
        bakery_data['baked goods'] = [baked_good.to_dict() for baked_good in bakery.baked_goods]
        response = make_response(jsonify(bakery_data))
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(jsonify({'meesage': 'Bakery not found'}))
        response.headers['Content-Type'] = 'application/json'
        return response
        
    

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_list = [baked_good.to_dict(rules=('-bakery.baked_goods',)) for baked_good in baked_goods]
    response = make_response(jsonify(baked_goods_list))
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if most_expensive:
        response = make_response(jsonify(most_expensive.to_dict(rules=('-bakery.baked_goods',))))
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(jsonify({'message': 'No baked goods found'}))
        response.headers['Content-Type'] = 'application/json'
        return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

# Add a route for creating a new bakery
@app.route('/bakeries', methods=['POST'])
def create_bakery():
    data = request.json
    name = data.get('name')
    if not name:
        return make_response(jsonify({'error': 'Name is required'}), 400)
    bakery = Bakery(name=name)
    db.session.add(bakery)
    db.session.commit()
    return make_response(jsonify(bakery.to_dict()), 201)

# Add a route for updating a bakery by ID
@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    data = request.json
    name = data.get('name')
    bakery = Bakery.query.get(id)
    if not bakery:
        return make_response(jsonify({'error': 'Bakery not found'}), 404)
    if name:
        bakery.name = name
    db.session.commit()
    return make_response(jsonify(bakery.to_dict()), 200)

# Add a route for deleting a bakery by ID
@app.route('/bakeries/<int:id>', methods=['DELETE'])
def delete_bakery(id):
    bakery = Bakery.query.get(id)
    if not bakery:
        return make_response(jsonify({'error': 'Bakery not found'}), 404)
    db.session.delete(bakery)
    db.session.commit()
    return make_response(jsonify({'message': 'Bakery deleted successfully'}), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)

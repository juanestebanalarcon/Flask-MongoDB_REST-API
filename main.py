from app import app, mongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request,make_response
from werkzeug.security import generate_password_hash, check_password_hash

def status200():
    return {'ok':True,'message':'Transaction successfully executed'}
@app.route('/add',methods=['POST'])
def add_user():
    _json = request.json
    _name = _json['name']
    _last_name = _json['last_name']
    _email = _json['email']
    _age = _json['age']
    _password = _json['passwrd']
    mongo.db.student.insert_one({'name': _name,'lastName':_last_name, 'age':_age,
                                           'email': _email,'password':generate_password_hash(_password)})
    return make_response(jsonify(status200()), 200)

@app.route('/students',methods=['GET'])
def get_students():
    _users_list = mongo.db.student.find()
    return make_response(dumps(_users_list),200)

@app.route('/student/<id>',methods=['GET'])
def get_student(id):
    _user = mongo.db.student.find_one({'_id':ObjectId(id)})
    return make_response(dumps(_user),200)

@app.route('/update/<id>',methods=['PUT'])
def update_student(id):
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _password = _json['current_passwrd']
    _new_password = _json['new_passwrd']
    _user = mongo.db.student.find_oone({'_id':ObjectId(id)})
    if _user.password == generate_password_hash(_password):
        mongo.db.student.update_one({'_id':ObjectId(id)},{'$set':{'name': _name,'email': _email,'password':generate_password_hash(_new_password)}})
        return make_response(jsonify(status200()), 200)
    else:
        return internal_server_error()
@app.route('/del/<id>',methods=['DELETE'])
def delete_student(id):
    mongo.db.student.delete_one({'_id':ObjectId(id)})
    return make_response(jsonify(status200()), 200)
@app.errorhandler(404)
def not_found(error = None):
    return make_response(jsonify({
        'status': 404,
        'message': f'Not Found {request.url}'
    }),404)
@app.errorhandler(400)
def bad_request(error = None):
    return make_response(jsonify({
        'status': 400,
        'message': f'Bad request {request.url}'
    }),400)
@app.errorhandler(500)
def internal_server_error(error = None):
    return make_response(jsonify({
        'status': 500,
        'message': f'Internal server error {request.url}'
    }),500)
if __name__ == '__main__':
    app.run()
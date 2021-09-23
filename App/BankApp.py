from config import client, DATABASE
from flask import request, jsonify, make_response
from App import app
import string,random


#dbase = client.BankSystem
collection = DATABASE['account']
@app.route("/api/create-user", methods=["POST"])
def add_user():

    try:
        rec = request.get_json()
        name = rec['name']
        email = rec['email']

        if not collection.find_one({"email": email}):
            account_id = ''.join(random.choice('0123456789abcdef') for n in range(34))
            record = {
                '_id': account_id,
                'name': name,
                'email': email,
                'state': rec['state'],
                'city': rec['city'],
                'address': rec['address'],
                'phone': rec['phone']
            }
            collection.insert_one(record)
            res = {
                'account_id': account_id
            }
            return make_response(jsonify({"Message": "Account Created. Remember the account number!!", "Account Number": account_id}), 201)
        else:
            res = {
                'message': 'It is an existing account!'
            }
            return make_response(jsonify(res), 200)

    except:
        res = {
            'message': 'Sorry!! Try again later.'
        }
        return make_response(jsonify(res), 503)


@app.route("/api/get-user/<account_id>", methods=["GET"])
def get_user(account_id):

    try:
        user = collection.find_one({'_id': account_id}, {'_id': 0})
        if user:
            res = {
                'data': user
            }
            return make_response(jsonify(res), 200)
        else:
            res = {
                'message': 'Bank account missing!!'
            }
            return make_response(jsonify(res), 404)

    except:
        res = {
            'message': 'Sorry!! Try again later.'
        }
        return make_response(jsonify(res), 503)


@app.route("/api/update-user/<account_id>", methods=['PUT'])
def update_user(account_id):

    try:
        if collection.find_one({"_id": account_id}):
            rec = request.get_json()
            new_values = {"$set": rec}
            collection.update_one({'_id': account_id}, new_values)
            res = {
                'message': 'Account Info Updated'
            }
            return make_response(jsonify(res), 200)
        else:
            res = {
                'message': 'Account user not found!!'
            }
            return make_response(jsonify(res), 404)

    except:
        res = {
            'message': 'Sorry!! Try again later.'
        }
        return make_response(jsonify(res), 503)


@app.route("/api/delete-user/<account_id>", methods=["DELETE"])
def delete_user(account_id):

    try:
        if collection.find_one({"_id":account_id}):
            collection.delete_one({'_id': account_id})
            res = {
                'message': 'Account has been deleted....Sorry to see you leave.'
            }
            return make_response(jsonify(res), 200)
        else:
            res={
                'message':'Trying to delete non existing account!!'
            }
    except:
        res = {
            'message': 'Sorry!! Try again later.'
        }
        return make_response(jsonify(res), 503)

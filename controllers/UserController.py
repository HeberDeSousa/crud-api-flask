from flask import Response, request, jsonify
from models.User import User, db
from flask_sqlalchemy import SQLAlchemy
import json
import traceback

def index():
    session = db.session()
    users = session.query(User).all()
    users_json = [user.serialize() for user in users]
    session.close()
    return Response(json.dumps(users_json))

def store():
    body = request.get_json()
    session = db.session()
    try:
        user = User(name = body['name'], age = body['age'], address = body['address'])
        session.add(user)
        session.commit()
        return Response(json.dumps(user.serialize()), status=201, mimetype='application/json')
    except Exception as e:
        session.rollback()
        error_message = str(e)
        # stack_trace = traceback.format_exc()
        return jsonify({"error": error_message}), 500 # , "stack_trace": stack_trace}), 500
    finally:
        session.close()

def update(user_id):
    body = request.get_json()
    if not isinstance(body, dict):
        return jsonify({"error": "Invalid input format, expected a JSON object"}), 400
    if 'name' in body and not isinstance(body['name'], str):
        return jsonify({"error": "Invalid data type for 'name', expected a string"}), 400
    if 'age' in body and not isinstance(body['age'], int):
        return jsonify({"error": "Invalid data type for 'age', expected an integer"}), 400
    if 'address' in body and not isinstance(body['address'], str):
        return jsonify({"error": "Invalid data type for 'address', expected a string"}), 400
    session = db.session()
    try:
        user = session.query(User).get(user_id)
        if user is None:
            return Response(), 404
        else:
            if body and body['name']:
                user.name = body['name']
            if body and body['age']:
                user.age = body['age']
            if body and body['address']:
                user.address = body['address']
            session.commit()
            return Response(json.dumps(user.serialize()), status=200, mimetype='application/json')
    except Exception as e:
        session.rollback()
        error_message = str(e)
        # stack_trace = traceback.format_exc()
        return jsonify({"error": error_message}), 500 # , "stack_trace": stack_trace}), 500
    finally:
        session.close()

def destroy(user_id):
    session = db.session()
    try:
        user = session.query(User).get(user_id)
        if user is None:
            return Response(), 404
        else:
            session.delete(user)
            session.commit()
            return Response(), 204
    except Exception as e:
        session.rollback()
        error_message = str(e)
        # stack_trace = traceback.format_exc()
        return jsonify({"error": error_message}), 500 # , "stack_trace": stack_trace}), 500
    finally:
        session.close()

def show(user_id):
    session = db.session()
    try:
        user = session.query(User).get(user_id)
        if user is None:
            return Response(), 404
        else:
            return Response(json.dumps(user.serialize()), status=200, mimetype='application/json')
    except Exception as e:
        session.rollback()
        error_message = str(e)
        # stack_trace = traceback.format_exc()
        return jsonify({"error": error_message}), 500 # , "stack_trace": stack_trace}), 500
    finally:
        session.close()
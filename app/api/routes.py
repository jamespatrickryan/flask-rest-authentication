from flask import abort, g, jsonify, request, url_for

from app import basic_auth, db
from app.api import blueprint
from app.models import User


@blueprint.route('/users', methods=('POST',))
def create_user():
    username = request.json.get('username')
    password = request.json.get('password')

    if username is None or password is None:
        abort(400)

    if User.query.filter_by(username=username).first() is not None:
        abort(400)

    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()

    return (jsonify({'username': user.username}), 201,
            {'Location': url_for('main.get_user', id=user.id, _external=True)})


@blueprint.route('/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})


@blueprint.route('/token')
@basic_auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token, 'duration': 600})


@blueprint.route('/resource')
@basic_auth.login_required
def get_resource():
    return jsonify({'data': f'Hello, {g.user.username}.'})

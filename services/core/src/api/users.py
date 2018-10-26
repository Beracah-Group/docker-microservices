import json
from flask_restful import Resource
from flask import request


class Users(Resource):
    """User resources, implements get, post, put, delete."""

    def __init__(self, **kwargs):
        self.User = kwargs['User']
        self.Location = kwargs['Location']

    def get(self, user_id=None):
        """Implement retrive user."""
        email = request.args.get('email')
        username = request.args.get('username')
        if not(user_id or username or email):
            users = [user.serialize() for user in self.User.query.all()]
            return {
                'users': users,
                'message': 'Successfully retrived all users'
            }, 200
        elif user_id:
            user = self.User.query.filter_by(uid=user_id).first()
        elif email:
            user = self.User.query.filter_by(email=email).first()
        elif username:
            user = self.User.query.filter_by(user_name=username).first()

        if not user:
            return {
                'message': f'User {user_id or email or username} not found'
            }, 404

        return {
            'user': user.serialize(),
            'message': 'Successfully retrived user'
        }, 200

    def post(self):
        """Implement create user."""
        payload = json.loads(request.data)

        name = payload.get('name')
        email = payload.get('email')
        user_name = payload.get('user_name')
        phone = payload.get('phone')

        if not (payload or all([name, email, user_name, phone])):
            return {
                'message': 'Please pass in name, username, phone, email, '
                'location'
            }, 400

        if any([self.User.query.filter_by(name=name).first(),
                self.User.query.filter_by(email=email).first(),
                self.User.query.filter_by(user_name=user_name).first(),
                self.User.query.filter_by(phone=phone).first()]):
            return {
                'message': 'User with some of those credetials already exists.'
            }, 400

        location = self.Location.query.filter_by(
            uid=payload.get('location')).first()

        new_user = self.User(
            name=payload.get('name'),
            user_name=payload.get('username'),
            photo=payload.get('photo', None),
            phone=payload.get('phone'),
            email=payload.get('email'),
            location=location
        )
        new_user.save()

        return {
            'user': new_user.serialize(),
            'message': 'User created succefully'
        }, 201

from flask import Blueprint, request, jsonify, current_app, url_for
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import User, UserRole, db
from app.schemas import user_schema
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from app import mail
from itsdangerous import URLSafeTimedSerializer, SignatureExpired


auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 400
    
    hashed_password = generate_password_hash(data['password'])
    
    # Check if admin registration code is provided and correct
    admin_code = data.get('admin_code')
    if admin_code and admin_code == current_app.config['ADMIN_REGISTRATION_CODE']:
        role = UserRole.ADMIN
    else:
        role = UserRole.USER

    new_user = User(
        username=data['username'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        password=hashed_password,
        email=data['email'],
        role=role
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully', 'role': role.value}), 201


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    
    return jsonify({'message': 'Invalid username or password'}), 401



def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='password-reset-salt')

def verify_reset_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=expiration)
    except SignatureExpired:
        return None
    return email

@auth.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')
    user = User.query.filter_by(email=email).first()
    if user:
        token = generate_reset_token(user.email)
        reset_url = url_for('auth.reset_password', token=token, _external=True)
        
        # Send email
        msg = Message('Password Reset Request',
                      sender='noreply@yourdomain.com',
                      recipients=[user.email])
        msg.body = f'''To reset your password, visit the following link:
{reset_url}

If you did not make this request then simply ignore this email and no changes will be made.
'''
        mail.send(msg)
        
        return jsonify({'message': 'Password reset link sent to your email.'}), 200
    return jsonify({'message': 'Email not found.'}), 404

@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == 'GET':
        # Here you would typically render a form for the user to enter a new password
        # Since we're working with an API, we'll just verify the token
        email = verify_reset_token(token)
        if email is None:
            return jsonify({'message': 'Invalid or expired token'}), 400
        return jsonify({'message': 'Token is valid', 'email': email}), 200
    
    elif request.method == 'POST':
        email = verify_reset_token(token)
        if email is None:
            return jsonify({'message': 'Invalid or expired token'}), 400
        
        user = User.query.filter_by(email=email).first()
        if user:
            data = request.get_json()
            new_password = data.get('new_password')
            if not new_password:
                return jsonify({'message': 'New password is required'}), 400
            
            hashed_password = generate_password_hash(new_password)
            user.password = hashed_password
            db.session.commit()
            return jsonify({'message': 'Password has been reset successfully'}), 200
        
        return jsonify({'message': 'User not found'}), 404
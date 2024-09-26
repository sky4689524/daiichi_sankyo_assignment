import jwt
from functools import wraps
from flask import request, jsonify
import os


def token_required(f):
    """
    Decorator to validate the JWT token sent in the Authorization header.

    If the token is valid, it proceeds with the request. Otherwise, it returns
    an appropriate error message (e.g., "Token is missing", "Invalid token").

    Args:
        f (function): The route function to wrap.

    Returns:
        function: The decorated function with token validation.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Retrieve token from Authorization header
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            # Decode the JWT token
            secret_key = os.getenv('JWT_SECRET_KEY')
            data = jwt.decode(token, secret_key, algorithms=['HS256'])
            current_user_role = data['r']  # Extract role from the token
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token!"}), 401

        return f(current_user_role, *args, **kwargs)

    return decorated_function


def role_required(required_role):
    """
    Decorator to enforce role-based access control.

    This decorator checks if the current user's role matches the required role
    for the route.

    Args:
        required_role (str): The role required to access the route.

    Returns:
        function: The decorated function with role validation.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(current_user_role, *args, **kwargs):
            if current_user_role != required_role:
                return jsonify({"message": "Access denied: Insufficient permissions!"}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

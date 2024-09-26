import jwt
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def generate_compact_token(role):
    """
    Generates a compact JWT token with a minimal payload.

    Args:
        role (str): The role to be included in the token, such as "admin" or "user".

    Returns:
        str: A compact JWT token as a string.

    Raises:
        ValueError: If JWT_SECRET_KEY is not set in the environment.
    """
    payload = {"r": role}  # Compact payload using 'r' for role

    # Load the JWT secret key from the environment variables
    secret_key = os.getenv('JWT_SECRET_KEY')
    if not secret_key:
        raise ValueError("JWT_SECRET_KEY environment variable is not set")

    # Generate and return the JWT token
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token.decode('utf-8') if isinstance(token, bytes) else token


# Generate compact tokens for admin and user
admin_token = generate_compact_token("admin")
user_token = generate_compact_token("user")

print(f"Admin Token: {admin_token}")
print(f"User Token: {user_token}")

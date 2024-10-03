from flask import Blueprint, jsonify
from ..utils.token_decorators import token_required, role_required

# Create a new blueprint for access control routes
access_blueprint = Blueprint('access', __name__)

@access_blueprint.route('/api/v1/user-access', methods=['GET'])
@token_required  # Validate the JWT token for any user
def user_access(current_user_role):
    """
    Route accessible by any user with a valid JWT token.
    
    Args:
        current_user_role (str): The role extracted from the validated JWT token.
    
    Returns:
        JSON response with a message confirming access for the user.
    """
    return jsonify({"message": f"Hello {current_user_role}, you have access to this route!"}), 200

@access_blueprint.route('/api/v1/admin-access', methods=['GET'])
@token_required  # Validate the JWT token
@role_required('admin')  # Only allow access for admin users
def admin_access():
    """
    Route accessible only by admin users.
    
    Returns:
        JSON response with a message confirming access for the admin.
    """
    return jsonify({"message": "Hello Admin, you have full access to this route!"}), 200

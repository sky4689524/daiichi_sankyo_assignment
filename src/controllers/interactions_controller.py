from flask import Blueprint, jsonify, request, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import OperationalError, ProgrammingError

# Create a new blueprint for interactions
interactions_blueprint = Blueprint('interactions', __name__)


def get_db_connection():
    """
    Establish a database connection using configuration from Flask's current app.

    Returns:
        psycopg2.connection: A connection object for PostgreSQL.

    Raises:
        OperationalError: If the connection to the database fails.
    """
    try:
        conn = psycopg2.connect(
            dbname=current_app.config['DB_NAME'],
            user=current_app.config['DB_USER'],
            password=current_app.config['DB_PASSWORD'],
            host=current_app.config['DB_HOST'],
            port=current_app.config['DB_PORT']
        )
        return conn
    except OperationalError as e:
        raise OperationalError(f"Database connection failed: {e}")


@interactions_blueprint.route('/api/v1/interactions/<int:customer_id>', methods=['GET'])
def get_customer_interactions(customer_id):
    """
    Retrieve and return the interaction counts for a specific customer.

    Args:
        customer_id (int): The ID of the customer whose interactions are to be retrieved.

    Returns:
        JSON: A response containing the interaction counts per channel (Email, Call, Bird).

    Raises:
        404: If the customer does not exist.
        500: If there is a database connection failure or SQL query error.
    """
    try:
        # Establish a database connection
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # Check if the customer exists in the database
        customer_query = "SELECT 1 FROM customers WHERE Customer_Id = %s;"
        cur.execute(customer_query, (customer_id,))
        customer_exists = cur.fetchone()

        if not customer_exists:
            return jsonify({"error": f"Customer with id {customer_id} not found"}), 404

        # Query to get the count of interactions per channel for the given customer
        query = """
        SELECT event, COUNT(*) as count
        FROM interactions
        WHERE customers = %s
        GROUP BY event;
        """
        cur.execute(query, (customer_id,))
        interactions = cur.fetchall()

        # Initialize default values for each interaction type
        response_data = {
            "customer_id": customer_id,
            "interactions": {
                "Email": 0,
                "Call": 0,
                "Bird": 0
            }
        }

        # Update the response with actual counts from the query result
        for interaction in interactions:
            event = interaction['event']
            count = interaction['count']
            if event in response_data['interactions']:
                response_data['interactions'][event] = count

        # Close the database connection
        cur.close()
        conn.close()

        return jsonify({"data": response_data}), 200

    except OperationalError as e:
        return jsonify({"error": "Database connection failed", "details": str(e)}), 500

    except ProgrammingError as e:
        return jsonify({"error": "Database query failed", "details": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

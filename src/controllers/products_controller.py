from flask import Blueprint, jsonify, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import OperationalError
from ..utils.token_decorators import token_required, role_required

# Create a new blueprint for products
products_blueprint = Blueprint('products', __name__)

def get_db_connection():
    """
    Establishes a connection to the PostgreSQL database using the configuration
    from the Flask app.

    Returns:
        psycopg2.connection: A connection object to the PostgreSQL database.
    
    Raises:
        RuntimeError: If there is an issue connecting to the database.
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
        raise RuntimeError(f"Database connection failed: {e}")


@products_blueprint.route('/api/v1/interactions/products', methods=['GET'])
@token_required  # Validate the JWT token
@role_required('admin')  # Only allow admin role access
def get_interactions_per_product():
    """
    Fetches and returns the count of interactions for each product, grouped by customer type.

    Returns:
        JSON: A response containing interaction counts per product for each customer type.
    
    Raises:
        500: If there is a database connection failure or other internal errors.
    """
    try:
        # Establish database connection
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # Fetch interaction counts grouped by customer type and product
        query = """
        SELECT
            c.type AS customer_type,
            p.product,
            COUNT(*) AS interaction_count
        FROM
            interactions i
        JOIN
            customers c ON i.customers = c.customer_id
        JOIN
            products p ON TO_CHAR(i.date_start, 'MM-YYYY') = p.date
        GROUP BY
            c.type,
            p.product
        ORDER BY
            c.type, p.product;
        """
        cur.execute(query)
        results = cur.fetchall()

        # Organize the results into the required JSON format
        data = {}
        for row in results:
            customer_type = row['customer_type']
            product = row['product']
            interaction_count = row['interaction_count']

            if customer_type not in data:
                data[customer_type] = []
            data[customer_type].append({
                "product": product,
                "interaction_count": interaction_count
            })

        # Convert data to a list for the final JSON response
        response_data = [
            {
                "customer_type": customer_type,
                "products": products
            }
            for customer_type, products in data.items()
        ]

        # Close the database connection
        cur.close()
        conn.close()

        # Return the final structured response
        return jsonify({"data": response_data}), 200

    except OperationalError as e:
        return jsonify({"error": "Database connection failed", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

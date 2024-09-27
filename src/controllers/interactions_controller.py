from flask import Blueprint, jsonify
from sqlalchemy import select
from ..db import db 

# Create a new blueprint for interactions
interactions_blueprint = Blueprint('interactions', __name__)

@interactions_blueprint.route('/api/v1/interactions/<int:customer_id>', methods=['GET'])
def get_customer_interactions(customer_id):
    """
    Retrieve and return the interaction counts (Email, Call, Bird) for a specific customer
    from the database using SQLAlchemy.

    Args:
        customer_id (int): The ID of the customer to retrieve interactions for.

    Returns:
        JSON: A response containing the interaction counts per event type.
    """
    try:

        customers_table = db.metadata.tables['customers']
        interactions_table = db.metadata.tables['interactions']

        stmt = select(customers_table).where(customers_table.c.customer_id == customer_id)
        customer = db.session.execute(stmt).fetchone()

        if not customer:
            return jsonify({"error": f"Customer with id {customer_id} not found"}), 404

        # Query to get the count of interactions per event (channel) for the given customer
        stmt = (
            select(interactions_table.c.event, db.func.count().label('count'))
            .where(interactions_table.c.customers == customer_id)
            .group_by(interactions_table.c.event)
        )
        interactions = db.session.execute(stmt).fetchall()

        
        response_data = {
            "customer_id": customer_id,
            "interactions": {
                "Email": 0,
                "Call": 0,
                "Bird": 0
            }
        }

        
        for interaction in interactions:
            event = interaction.event
            count = interaction.count
            if event in response_data['interactions']:
                response_data['interactions'][event] = count

        return jsonify({"data": response_data}), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

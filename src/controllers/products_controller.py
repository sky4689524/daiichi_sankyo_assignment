from flask import Blueprint, jsonify
from sqlalchemy import select
from ..db import db 

# Create a new blueprint for products
products_blueprint = Blueprint('products', __name__)

@products_blueprint.route('/api/v1/interactions/products', methods=['GET'])
def get_interactions_per_product():
    """
    Fetches and returns the count of interactions for each product, grouped by customer type
    from the database using SQLAlchemy.

    Returns:
        JSON: A response containing interaction counts per product for each customer type.
    """
    try:
       
        customers_table = db.metadata.tables['customers']
        interactions_table = db.metadata.tables['interactions']
        products_table = db.metadata.tables['products']

        
        query = (
            select(
                customers_table.c.type.label('customer_type'),
                products_table.c.product,
                db.func.count().label('interaction_count')
            )
            .join(interactions_table, customers_table.c.customer_id == interactions_table.c.customers)
            .join(products_table, db.func.to_char(interactions_table.c.date_start, 'MM-YYYY') == products_table.c.date)
            .group_by(customers_table.c.type, products_table.c.product)
            .order_by(customers_table.c.type, products_table.c.product)
        )

        
        results = db.session.execute(query).fetchall()

        
        data = {}
        for row in results:
            customer_type = row.customer_type
            product = row.product
            interaction_count = row.interaction_count

            if customer_type not in data:
                data[customer_type] = []
            data[customer_type].append({
                "product": product,
                "interaction_count": interaction_count
            })

        
        response_data = [
            {
                "customer_type": customer_type,
                "products": products
            }
            for customer_type, products in data.items()
        ]

        
        return jsonify({"data": response_data}), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

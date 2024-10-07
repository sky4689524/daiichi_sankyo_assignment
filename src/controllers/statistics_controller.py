from flask import Blueprint, jsonify
from ..db import db

# Define valid tables to check
VALID_TABLES = ["customers", "products", "interactions"]

# Create a new blueprint for statistics
stats_blueprint = Blueprint("stats_blueprint", __name__)


@stats_blueprint.route("/api/v1/stats/<table_name>", methods=["GET"])
def table_count(table_name):
    """
    Returns the number of rows in the given table if the table exists.

    Args:
        table_name (str): The name of the table.

    Returns:
        JSON: A JSON response containing the number of rows or an error message.
    """

    if table_name not in VALID_TABLES:
        return jsonify({"message": "Table name not found"}), 404

    try:

        table = db.metadata.tables.get(table_name)

        # If the table exists in the metadata, perform a count query
        if table is not None:

            stmt = db.session.query(db.func.count()).select_from(table)
            row_count = db.session.execute(stmt).scalar()

            return jsonify({"message": "Number of Rows", "rows": row_count}), 200
        else:

            return jsonify({"message": "Table not found in the database"}), 404

    except Exception as e:

        return jsonify({"message": "Internal server error", "details": str(e)}), 500

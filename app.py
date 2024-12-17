from flask import Flask, jsonify, request, abort
from jsonschema import validate, ValidationError

app = Flask(__name__)

# Sample in-memory data storage (in a real-world scenario, use a database)
records = {
    1: {"name": "John Doe", "age": 30, "email": "john@example.com"},
    2: {"name": "Jane Smith", "age": 25, "email": "jane@example.com"}
}

# JSON schema for validating input data
record_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer"},
        "email": {"type": "string", "format": "email"}
    },
    "required": ["name", "age", "email"],
    "additionalProperties": False
}

# Fetch all records
@app.route('/records', methods=['GET'])
def get_records():
    return jsonify(records), 200

# Add a new record
@app.route('/records', methods=['POST'])
def add_record():
    data = request.get_json()

    # Validate the input data using the JSON schema
    try:
        validate(instance=data, schema=record_schema)
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400

    record_id = len(records) + 1
    records[record_id] = data
    return jsonify({"id": record_id, "record": data}), 201

# Update a record by ID
@app.route('/records/<int:id>', methods=['PUT'])
def update_record(id):
    if id not in records:
        abort(404, description="Record not found")

    data = request.get_json()

    # Validate the input data using the JSON schema
    try:
        validate(instance=data, schema=record_schema)
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400

    records[id] = data
    return jsonify({"id": id, "record": data}), 200

# Delete a record by ID
@app.route('/records/<int:id>', methods=['DELETE'])
def delete_record(id):
    if id not in records:
        abort(404, description="Record not found")

    del records[id]
    return jsonify({"message": "Record deleted successfully"}), 200

# Error handler for record not found
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": error.description}), 404

if __name__ == '__main__':
    app.run(debug=True)

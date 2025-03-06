import os
from flask import request, jsonify
from bson import ObjectId
from Mongodb.client import get_Client

def get_collection():
    try:
        collection_name = os.environ["X-mongo-collection"]
        my_client = get_Client()
        collection = my_client["data_db"][collection_name]
        return collection
    except KeyError:
        raise KeyError("Environment variable 'X-mongo-collection' not set")
    except Exception as e:
        raise ConnectionError(f"Error getting collection: {str(e)}")

def handle_request_data():
    data = request.get_json()
    if not data:
        return None, jsonify({"error": "No data provided"}), 400
    return data, None, None

def insert_data():
    data, error_response, status_code = handle_request_data()
    if error_response:
        return error_response, status_code

    try:
        collection = get_collection()
        request_data = data.get('data')
        if request_data is None:
            return jsonify({"error": "No data provided"}), 400
        result = collection.insert_one(dict(request_data))
        return jsonify({"message": f"Data inserted successfully on {os.environ['X-mongo-collection']}"}), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500

def update_data_by_id():
    data, error_response, status_code = handle_request_data()
    if error_response:
        return error_response, status_code

    try:
        document_id = data.get('id')
        try:
            document_id = ObjectId(document_id)
        except Exception:
            return jsonify({"error": "Invalid Document ID format"}), 400
        if not document_id:
            return jsonify({"error": "Document ID cannot be empty"}), 400
        new_values = data.get('data')
        if new_values is None:
            return jsonify({"error": "No data provided to update"}), 400

        collection = get_collection()
        result = collection.update_one({"_id": document_id}, {"$set": dict(new_values)})
        if result.modified_count == 0:
            return jsonify({"message": "Document found but no changes were made"}), 200
        return jsonify({"message": "Data updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def update_data():
    data, error_response, status_code = handle_request_data()
    if error_response:
        return error_response, status_code

    try:
        collection = get_collection()
        filter_criteria = data.get('filter', {})
        new_values = {"$set": data.get('new_data', {})}
        result = collection.update_one(filter_criteria, new_values)
        if result.matched_count == 0:
            return jsonify({"message": "No matching document found"}), 404
        return jsonify({"message": "Data updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def delete_data():
    data, error_response, status_code = handle_request_data()
    if error_response:
        return error_response, status_code

    try:
        collection = get_collection()
        filter_criteria = data.get('filter', {})
        result = collection.delete_one(filter_criteria)
        if result.deleted_count == 0:
            return jsonify({"message": "No matching document found"}), 404
        return jsonify({"message": "Data deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_all_data():
    try:
        collection = get_collection()
        documents = list(collection.find())
        for document in documents:
            document['_id'] = str(document['_id'])
        return jsonify({"data": documents}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_data_by_id():
    data, error_response, status_code = handle_request_data()
    if error_response:
        return error_response, status_code

    try:
        collection = get_collection()
        document_id = data.get('id')
        try:
            document_id = ObjectId(document_id)
        except Exception:
            return jsonify({"error": "Invalid Document ID format"}), 400
        document = collection.find_one({"_id": document_id})
        if document:
            document['_id'] = str(document['_id'])
        return jsonify({"data": document}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_data_by_filter():
    data, error_response, status_code = handle_request_data()
    if error_response:
        return error_response, status_code

    try:
        collection = get_collection()
        filter_criteria = data.get('filter', {})
        documents = list(collection.find(filter_criteria))
        if not documents:
            return jsonify({"message": "No matching documents found"}), 404
        for document in documents:
            document['_id'] = str(document['_id'])
        return jsonify({"data": documents}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def render_mongo_data_pack(app):
    @app.before_request
    def before_request():
        try:
            collection_name = request.headers.get('X-mongo-collection')
            if collection_name:
                os.environ["X-mongo-collection"] = collection_name
            print(f"X-mongo-collection: {collection_name}")
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    app.add_url_rule('/insert-data', 'create_collection_api', insert_data, methods=['POST'])
    app.add_url_rule('/update-data-by-id', 'update_data_by_id_api', update_data_by_id, methods=['POST'])
    app.add_url_rule('/update-data', 'update_data_api', update_data, methods=['POST'])
    app.add_url_rule('/get-data-by-id', 'get_data_by_id_api', get_data_by_id, methods=['POST'])
    app.add_url_rule('/get-data-by-filter', 'get_data_by_filter_api', get_data_by_filter, methods=['POST'])
    app.add_url_rule('/delete-data', 'delete_data_api', delete_data, methods=['DELETE'])
    app.add_url_rule('/get-all-data', 'get_all_data_api', get_all_data, methods=['GET'])

    return app

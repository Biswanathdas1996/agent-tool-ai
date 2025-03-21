from sentence_transformers import SentenceTransformer
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from pymongo.operations import SearchIndexModel
import time
from flask import request, jsonify
from Mongodb.client import get_client
import logging

logging.basicConfig(level=logging.INFO)

def get_collection(collection_name):
    try:
        my_client = get_client()
        collection = my_client["rag_db"][collection_name]
        return collection
    except Exception as e:
        logging.error(f"Error getting collection: {str(e)}")
        raise

def get_embedding(data, model):
    try:
        embedding = model.encode(data)
        return embedding.tolist()
    except Exception as e:
        logging.error(f"Error generating embedding: {str(e)}")
        raise

def save_temp_file(files, folder_path):
    if not files:
        return "Got no file for processing"
    file_paths = []
    for file in files:
        file_path = os.path.join(folder_path, file.filename)
        try:
            file.save(file_path)
            file_paths.append(file_path)
        except Exception as e:
            logging.error(f"An error occurred while saving the file: {str(e)}")
            return f"An error occurred while saving the file: {str(e)}"
    return file_paths

def process_files(files_path):
    data = []
    for path in files_path:
        if os.path.exists(path) and os.path.getsize(path) > 0:
            loader = PyPDFLoader(path)
            data.extend(loader.load())
        else:
            raise FileNotFoundError(f"File {path} not found or is empty.")
    return data

def upload_file_to_mongo_db(files, save_file_path, collection_name):
    try:
        files_path = save_temp_file(files, save_file_path)
        data = process_files(files_path)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=20)
        documents = text_splitter.split_documents(data)
        logging.info(f"Number of documents: {len(documents)}")
        model = SentenceTransformer("nomic-ai/nomic-embed-text-v1", trust_remote_code=True)
        docs_to_insert = [{
            "text": doc.page_content,
            "embedding": get_embedding(doc.page_content, model),
            "page_number": doc.metadata["page"] + 1,
            "doc_name": doc.metadata["source"]
        } for doc in documents]

        collection = get_collection(collection_name)
        result = collection.insert_many(docs_to_insert)
        return result
    except Exception as e:
        logging.error(f"An error occurred while inserting documents: {str(e)}")
        return f"An error occurred while inserting documents: {str(e)}"

def indexing(collection_name):
    try:
        collection = get_collection(collection_name)
        search_index_model = SearchIndexModel(
            definition={
                "fields": [
                    {
                        "type": "vector",
                        "numDimensions": 768,
                        "path": "embedding",
                        "similarity": "cosine"
                    }
                ]
            },
            name=collection_name,
            type="vectorSearch"
        )
        collection.create_search_index(model=search_index_model)
        logging.info("Polling to check if the index is ready. This may take up to a minute.")
        predicate = lambda index: index.get("queryable") is True

        while True:
            indices = list(collection.list_search_indexes(collection_name))
            if len(indices) and predicate(indices[0]):
                break
            time.sleep(5)
        logging.info(f"{collection_name} is ready for querying.")
    except Exception as e:
        logging.error(f"Error indexing collection: {str(e)}")
        raise

def get_query_results(query, index_name, no_of_results=5):
    try:
        model = SentenceTransformer("nomic-ai/nomic-embed-text-v1", trust_remote_code=True)
        collection = get_collection(index_name)
        query_embedding = get_embedding(query, model)
        pipeline = [
            {
                "$vectorSearch": {
                    "index": index_name,
                    "queryVector": query_embedding,
                    "path": "embedding",
                    "exact": True,
                    "limit": no_of_results
                }
            }, {
                "$project": {
                    "_id": 0,
                    "text": 1,
                    "page_number": 1,
                    "doc_name": 1
                }
            }
        ]
        results = collection.aggregate(pipeline)
        return list(results)
    except Exception as e:
        logging.error(f"Error getting query results: {str(e)}")
        raise

def collection_names():
    try:
        collection = get_collection("any")
        indexes = collection.database.list_collection_names()
        logging.info(indexes)
        return indexes
    except Exception as e:
        logging.error(f"Error listing indexes: {str(e)}")
        raise

def upload_files_data_mongo_api():
    try:
        if 'files' not in request.files:
            return "No files provided", 400
        collection_name = request.form.get('collection_name')
        files = request.files.getlist('files')
        upload_file_to_mongo_db(files, 'mongodb/uploads', collection_name)
        return jsonify({"message": f"Data inserted successfully for {collection_name}"}), 200
    except Exception as e:
        logging.error(f"Error in upload_files_data_mongo_api: {str(e)}")
        return jsonify({"error": str(e)}), 500

def index_collextion_mongo_api():
    try:
        collection_name = request.form.get('collection_name')
        indexing(collection_name)
        return jsonify({"message": f"{collection_name} successfully indexed "}), 200
    except Exception as e:
        logging.error(f"Error in index_collextion_mongo_api: {str(e)}")
        return jsonify({"error": str(e)}), 500

def delete_collection_mongo_api():
    try:
        collection_name = request.form.get('collection_name')
        collection = get_collection(collection_name)
        collection.drop()
        return jsonify({"message": f"{collection_name} successfully deleted"}), 200
    except Exception as e:
        logging.error(f"Error in delete_collection_mongo_api: {str(e)}")
        return jsonify({"error": str(e)}), 500

def list_all_index_api():
    try:
        result = collection_names()
        return jsonify({"collections": result}), 200
    except Exception as e:
        logging.error(f"Error in list_all_index_api: {str(e)}")
        return jsonify({"error": str(e)}), 500

def get_query_results_mongo_api():
    try:
        data = request.get_json()
        query = data.get('query')
        no_of_results = data.get('no_of_results')
        collection_name = data.get('collection_name')
        result = get_query_results(query, collection_name, no_of_results)
        return jsonify({"results": result}), 200
    except Exception as e:
        logging.error(f"Error in get_query_results_mongo_api: {str(e)}")
        return jsonify({"error": str(e)}), 500

def render_mongo_pack(app):
    app.add_url_rule('/upload-collection-doc-mongo', 'upload_files_data_mongo', upload_files_data_mongo_api, methods=['POST'])
    app.add_url_rule('/indexing-mongo', 'index_collextion_mongo', index_collextion_mongo_api, methods=['POST'])
    app.add_url_rule('/delete-collection', 'delete_collection_mongo', delete_collection_mongo_api, methods=['POST'])
    app.add_url_rule('/list-index-mongo', 'list_all_index', list_all_index_api, methods=['GET'])
    app.add_url_rule('/get-context-mongo', 'get_query_results_mongo', get_query_results_mongo_api, methods=['POST'])
    return app 
